from xhtml2pdf import pisa

def html_2_pdf(request, pk):
    html = render_to_string(template_path, context)
    io_bytes = BytesIO()
    # write_to_file = open('uploads/payment_request/paper_form.pdf', 'w+b')
    # result = pisa.CreatePDF(html.encode("UTF-8"), dest=write_to_file)
    # write_to_file.close()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)
    
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse(pdf.err)

    """
    response = HttpResponse(content_type='application/pdf') # Create a Django response object, and specify content_type as pdf
    response['Content-Disposition'] = 'attachment; filename="paper_form.pdf"'
    pisa_status = pisa.CreatePDF( # create a pdf
       html, 
       dest=response, 
       # dest=BytesIO(),
       # link_callback=link_callback,
       )

    if pisa_status.err: # if error then show some funny view
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response
    """
