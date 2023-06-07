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


class InstanceOwnerUpdate(LoginRequiredMixin, UpdateView):
    model = Instance
    fields = ['owner']  # fields = '__all__'
    template_name = 'nanoassets/instance_update_owner.html'
    success_url = reverse_lazy('nanoassets:supported-instance-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owners = []
        for owner in User.objects.all():
            if owner.username != 'admin' and 'tishmanspeyer.com' in owner.email:
                # owners.append(owner)
                owners.append('%s ( %s )' % (owner.get_full_name(), owner.username))
        context['owners'] = owners
        return context

    def form_valid(self, form):
        original_instance = get_object_or_404(Instance, pk=form.instance.pk)
        assign_to = form.cleaned_data['owner'].strip(")").split("(")[-1].strip()

        if assign_to == 'admin':
            form.instance.owner = original_instance.owner
            messages.warning(self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
        elif assign_to == '' and original_instance.owner == None:
            form.instance.owner = original_instance.owner
            messages.warning(self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
        elif assign_to == '' and original_instance.owner:
            form.instance.status = 'AVAILABLE'  # self.object.status = 'AVAILABLE'
            self.object.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Returned from ' + original_instance.owner.username + ' by ' + self.request.user.get_full_name())
            messages.info(self.request, 'the IT Assets [ ' + original_instance.serial_number +
                          ' ] was Returned from ' + original_instance.owner.username)
        else:
            try:
                form.instance.owner = User.objects.get(username=assign_to)
            except User.DoesNotExist:
                form.instance.owner = None

            if not original_instance.owner:
                if not form.instance.owner:
                    form.instance.owner = original_instance.owner
                    messages.warning(self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
                elif assign_to == "":
                    form.instance.owner = original_instance.owner
                    messages.warning(self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
                else:
                    form.instance.status = 'inUSE'  # self.object.status = 'inUSE'
                    self.object.activityhistory_set.create(
                        description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Assigned to ' + form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 ') + ' by ' + self.request.user.get_full_name())
                    messages.info(self.request, 'the IT Assets [' + original_instance.serial_number + '] was Assign to ' +
                                form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 '))
            else:
                if not form.instance.owner:
                    form.instance.owner = original_instance.owner
                    messages.warning(
                        self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
                elif assign_to == original_instance.owner.username:
                    form.instance.owner = original_instance.owner
                    messages.warning(
                        self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
                else:
                    form.instance.status = 'inUSE'  # self.object.status = 'inUSE'
                    self.object.activityhistory_set.create(
                        description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Assigned to ' + form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 ') + ' by ' + self.request.user.get_full_name())
                    messages.info(self.request, 'the IT Assets [' + original_instance.serial_number + '] was Assign to ' +
                                form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 '))

        # url_back = self.request.META.get('HTTP_REFERER')
        
        return super().form_valid(form)
