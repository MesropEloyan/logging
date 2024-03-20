from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Document, DocumentHistory
from .forms import DocumentForm



@login_required(login_url='/admin/')
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            DocumentHistory.objects.create(document=document, action="Created", user=request.user)
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'document_create.html', {'form': form})

@login_required
def document_detail(request, pk):
    document = Document.objects.get(pk=pk)
    history = DocumentHistory.objects.filter(document=document)
    return render(request, 'document_detail.html', {'document': document, 'history': history})


@login_required
def document_edit(request, pk):
    document = Document.objects.get(pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)

        if form.is_valid():
            changed_fields = []
            for field in Document._meta.fields:
                if field.name in form.changed_data:
                    changed_fields.append(field.name)

            # Сохраняем первоначальные значения полей перед сохранением формы
            before_edits = {}
            for field_name in changed_fields:
                before_edits[field_name] = form.initial[field_name]
            
            # Сохраняем документ после получения первоначальных значений
            document = form.save()
            
            for field_name in changed_fields:
                after_edit = form.cleaned_data[field_name]
                DocumentHistory.objects.create(
                    document=document,
                    action="Edited",
                    user=request.user,
                    field_name=field_name,
                    before_edit=before_edits[field_name],
                    after_edit=after_edit,
                )
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_edit.html', {'form': form, 'document': document})


@login_required
def document_delete(request, pk):
    document = Document.objects.get(pk=pk)
    document.delete()
    # DocumentHistory.objects.create(document=document, action="Deleted", user=request.user)
    return redirect('document_list')
