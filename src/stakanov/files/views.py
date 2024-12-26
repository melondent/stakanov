from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import FileInfo
from collect.stakanov_logic import Indiana
import os
import uuid


def get_last_run_id(request):
    """Retrieves the last run ID from the session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        str or None: The run ID from the session, or None if no run ID is found.
    """
    return request.session.get('last_run_id')

def index(request):
    """Handles the index page, allowing for file scanning and showing the total
    file size. If the request method is POST, it starts the scanning process
    for the specified folder. The folder path must be provided, and if it is
    valid, the scanning process is initiated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse or HttpResponse: Returns a JSON response on POST with scan results or errors,
        or renders the 'index.html' template with total size information.
    """
    if request.method == "POST":
        folder = request.POST.get('folder')
        if not folder:
            return JsonResponse({"status": "error", "message": "Путь к папке не указан"})
        if os.path.exists(folder):
            try:
                run_id = str(uuid.uuid4())
                
                indiana = Indiana(folder, 'output.csv')
                indiana.find_loot()
                indiana.save_to_db(run_id=run_id)

                request.session['last_run_id'] = run_id 
                
                return JsonResponse({"status": "success", "message": "Сканирование завершено успешно! :-)"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Ошибка сканирования: {str(e)}"})
        else:
            return JsonResponse({"status": "error", "message": "Папка не найдена )-:"})
    
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
                
                
    context = {
        'total_size': total_size / (1024 ** 3),
                }
    
    return render(request, 'files/index.html', context)


def extension(request):
    """Displays statistics about file extensions for the last scan run.
    Retrieves the total size of all files and the size of files from the last
    run. Also gathers statistics on the number of occurrences of each file
    extension.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'extension.html' template with the relevant statistics.
    """
    run_id = get_last_run_id(request)
    if not run_id:
        return render(request, 'files/error.html', {'error': "Запустите приложение для получения статистики."})
    
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
    total_size_last = FileInfo.objects.filter(run_id=run_id).aggregate(Sum('size'))['size__sum'] or 0
    extension_stats = FileInfo.objects.filter(run_id=run_id).values('extension').annotate(count=Count('extension')).order_by('-count')
    
    context = {
        'total_size': total_size / (1024 ** 3),
        'total_size_last': total_size_last / (1024 ** 3),
        'extension_stats': extension_stats,
    }
    
    return render(request, 'files/extension.html', context)

def pdf(request):
    """Displays statistics for PDF files, specifically focusing on the top
    documents by page count. Retrieves the total size of all files and the
    total size from the last scan, and also displays the top 10 PDF files with
    the most pages.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'pdf.html' template with PDF statistics.
    """
    run_id = get_last_run_id(request)
    if not run_id:
        return render(request, 'files/error.html', {'error': "Запустите приложение для получения статистики."})
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
    total_size_last = FileInfo.objects.filter(run_id=run_id).aggregate(Sum('size'))['size__sum'] or 0
    top_documents = FileInfo.objects.filter(run_id=run_id, pages__isnull=False).order_by('-pages')[:10]
    
    
    context = {
        'total_size': total_size / (1024 ** 3),
        'total_size_last': total_size_last / (1024 ** 3),
        'top_documents': top_documents,
    }
    
    return render(request, 'files/pdf.html', context)

def image(request):
    """Displays statistics for image files, specifically focusing on the top
    images by area. Retrieves the total size of all files and the total size
    from the last scan, and also displays the top 10 images by area (width x
    height).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'image.html' template with image statistics.
    """
    run_id = get_last_run_id(request)
    if not run_id:
        return render(request, 'files/error.html', {'error': "Запустите приложение для получения статистики."})
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
    total_size_last = FileInfo.objects.filter(run_id=run_id).aggregate(Sum('size'))['size__sum'] or 0
    top_images = FileInfo.objects.filter(run_id=run_id, area__isnull=False).order_by('-area')[:10]
    
    context = {
        'total_size': total_size / (1024 ** 3),
        'total_size_last': total_size_last / (1024 ** 3),
        'top_images': top_images,
    }
    
    return render(request, 'files/image.html', context)

def size(request):
    """Displays statistics for the largest files, focusing on the top 10
    largest files by size. Retrieves the total size of all files and the total
    size from the last scan, and also displays the top 10 largest files.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'size.html' template with size statistics.
    """
    run_id = get_last_run_id(request)
    if not run_id:
        return render(request, 'files/error.html', {'error': "Запустите приложение для получения статистики."})
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
    total_size_last = FileInfo.objects.filter(run_id=run_id).aggregate(Sum('size'))['size__sum'] or 0
    top_files = FileInfo.objects.filter(run_id=run_id).order_by('-size')[:10]
    
    context = {
        'total_size': total_size / (1024 ** 3),
        'total_size_last': total_size_last / (1024 ** 3),
        'top_files': top_files,
    }
    
    return render(request, 'files/size.html', context)

def error(request):
    """Displays the error page with the total size of all files. This is shown
    when no valid scan run exists or an error occurs during processing.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'error.html' template with error information.
    """
    total_size = FileInfo.objects.aggregate(Sum('size'))['size__sum'] or 0
   
    context = {
        'total_size': total_size / (1024 ** 3),
    }
    
    return render(request, 'files/error.html', context)
