# from inertia import render, inertia
# # from django.shortcuts import render
# from django.http import JsonResponse


# # @inertia('App')
# # def index_from_inertia(request):
# #     return {
# #         'events': 'ANYTHING',
# #     }

# # def index_from_inertia(request):
# #     data = {}
# #     data['first'] = 'Amr'
# #     data['last'] = 'Amer'
# #     # if data['first'] == 'Amr':
# #     #     return JsonResponse(data)
    
# #     return render(
# #         request,
# #         'index.html',
# #         context={
# #             'var': 'Hello from INERTIA'
# #         }
# #     )
    
    
# def index_from_inertia(request):
#     props={
#         'events': 'Hello from INERTIA FROM DJANGO',
#         'role': request.user.role,
#     }
#     # template_data={
#     #     'temp': 'template data',  
#     # }
#     return render(
#         request=request,
#         component='Index',
#         props=props,
#         # template_data=template_data
#     )



# def app_page(request):
#     data = {}
#     data['role'] = request.user.role
    
#     return JsonResponse(data)
#     # return render(
#     #     request=request,
#     #     component='App',
#     #     props={},
#     #     # template_data=template_data
#     # )
