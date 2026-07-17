from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Import the new selector!
from apps.plugin_rbac.selectors.permissions import get_user_allowed_permissions

class DynamicNavigationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Get the allowed permissions dictionary from our selector
        allowed_permissions = get_user_allowed_permissions(request.user, request.auth)

        if not allowed_permissions:
            return Response({"navigation": []}, status=200)

        # 2. Group by Plugin (Tab) and Permission (Sub-tab) for the UI
        nav_dict = {}
        
        for perm in allowed_permissions.values():
            plugin_name = perm.plugin.name 
            
            if plugin_name not in nav_dict:
                nav_dict[plugin_name] = {
                    "name": plugin_name,
                    "subItems": []
                }
            
            sub_tab_name = perm.tab_name if perm.tab_name and perm.tab_name.strip().lower() != 'none' else perm.name

            nav_dict[plugin_name]["subItems"].append({
                "name": sub_tab_name,
                "href": perm.suburl
            })

        final_navigation = list(nav_dict.values())
        return Response({"navigation": final_navigation}, status=200)