from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.plugin_rbac.models import Plugin

from apps.saas_core_admin.selectors import subscription as billing_selectors
from apps.saas_core_admin.services import subscription as billing_services
from apps.plugin_rbac.permissions.navigation import HasRBACPermission

class SubscriptionPluginDashboardView(APIView):
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_rbac_permission = "Subscription Management"

    def get(self, request):
        """Get subscription and plugin status"""
        try:
            data = billing_selectors.get_admin_billing_dashboard(request.user)
            return Response({
                "status": True,
                "data": data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Activate a new plugin"""
        try:
            plugin_id = request.data.get('plugin_id')
            activated_plugin_data = billing_services.activate_plugin_for_admin(request.user, plugin_id)
            
            return Response({
                "status": True,
                "message": f"Successfully activated {activated_plugin_data['name']}",
                "plugin": activated_plugin_data
            }, status=status.HTTP_201_CREATED)
            
        except Plugin.DoesNotExist:
            return Response({"status": False, "message": "Plugin not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)