import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger('ibitsofphysics.requests')


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests with detailed information about:
    - Endpoint and HTTP method
    - Request parameters (GET/POST)
    - User information (authenticated/anonymous)
    - Request metadata (IP, User-Agent, etc.)
    - Response status and processing time
    """
    
    def process_request(self, request):
        """Log incoming request details"""
        request._start_time = time.time()
        
        # Get user information
        user_info = self._get_user_info(request)
        
        # Get request parameters
        get_params = dict(request.GET) if request.GET else {}
        post_params = self._get_post_params(request)
        
        # Get client information
        client_info = self._get_client_info(request)
        
        # Log the request
        user_str = f"{user_info['username']} (ID: {user_info['id']})" if user_info['authenticated'] else 'anonymous'
        logger.info(
            f"INCOMING REQUEST: {request.method} {request.get_full_path()} | User: {user_str} | IP: {client_info['ip_address']} | UA: {client_info['user_agent'][:50]}..."
        )
    
    def process_response(self, request, response):
        """Log response details and processing time"""
        if hasattr(request, '_start_time'):
            processing_time = time.time() - request._start_time
            user_info = self._get_user_info(request)
            user_str = f"{user_info['username']} (ID: {user_info['id']})" if user_info['authenticated'] else 'anonymous'
            
            logger.info(
                f"REQUEST COMPLETED: {request.method} {request.path} | Status: {response.status_code} | Time: {round(processing_time * 1000, 2)}ms | User: {user_str}"
            )
        
        return response
    
    def process_exception(self, request, exception):
        """Log exceptions that occur during request processing"""
        if hasattr(request, '_start_time'):
            processing_time = time.time() - request._start_time
            user_info = self._get_user_info(request)
            user_str = f"{user_info['username']} (ID: {user_info['id']})" if user_info['authenticated'] else 'anonymous'
            
            logger.error(
                f"REQUEST EXCEPTION: {request.method} {request.path} | Exception: {type(exception).__name__}: {str(exception)} | Time: {round(processing_time * 1000, 2)}ms | User: {user_str}",
                exc_info=True
            )
    
    def _get_user_info(self, request):
        """Extract user information from request"""
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            return {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
                'authenticated': True,
            }
        else:
            return {
                'authenticated': False,
                'type': 'anonymous'
            }
    
    def _get_post_params(self, request):
        """Extract POST parameters, handling sensitive data"""
        if not request.POST:
            return {}
        
        # List of sensitive fields to mask
        sensitive_fields = ['password', 'token', 'secret', 'key', 'csrf']
        
        post_params = {}
        for key, value in request.POST.items():
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                post_params[key] = '[MASKED]'
            else:
                post_params[key] = value
        
        return post_params
    
    def _get_client_info(self, request):
        """Extract client information from request headers"""
        return {
            'ip_address': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
            'accept_language': request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
            'host': request.META.get('HTTP_HOST', ''),
        }
    
    def _get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
