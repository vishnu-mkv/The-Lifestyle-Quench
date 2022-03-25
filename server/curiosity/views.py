from django.shortcuts import render


class Route:
    def __init__(self, url, methods, desc, permission):
        self.url = url
        self.methods = methods
        self.desc = desc
        self.permission = permission

    def __str__(self):
        return self.url


allRoutes = [
    Route("/api/users/activate/",
          ['POST'], "Activate user account using activation key.", "Public"),
    Route("/api/users/apply/", ['GET', 'POST', 'PATCH'],
          "Users can apply to be a writer", "User"),
    Route("/api/users/apply/history/",
          ['GET'], "get your previously submitted writer applications", "User"),
    Route("/api/users/apply/pending/",
          ['GET'], "Get your currently pending writer application", "User"),
    Route("/api/users/change-password/",
          ['POST'], "Change your account password using current password", "User"),
    Route("/api/users/contact-us/",
          ['POST'], "User can provide their email, name and contact", "Public"),
    Route("/api/users/forgot-password/change-password/",
          ['POST'], "Change password using forgot password key", "Public"),
    Route("/api/users/forgot-password/get-user/ ",
          ['GET'], "Get user associated with the forgot password key", "Public"),
    Route("/api/users/forgot-password/send-email/",
          ['POST'], "Sends forgot password key in email", "Public"),
    Route("/api/users/login/",
          ['POST'], "Get Auth Token using email and password", "Public"),
    Route("/api/users/posts/", ['GET'], "Get posts by user", "Writer"),
    Route("/api/users/profile/ ", ['GET', 'PATCH'],
          "Get your profile data", "Public"),
    Route("/api/users/register/",
          ['POST'], "Register and create an account. Activation mail will be sent", "Public"),
    Route("/api/users/resend-activation/",
          ['POST'], "Resend link to activate your account", "Public"),
    Route("/api/users/writer-profile/",
          ['GET'], "Get your writer profile", "Writer"),
    Route("/api/users/writer-profile/<writer_name>/",
          ['GET'], "Get writer profile using writer ID", "User"),
    Route("/check-availability/email/",
          ['POST'], "Check availability for email in registration", "Public"),
    Route("/check-availability/writer-name/",
          ['POST'], "Check availability for writer ID", "User"),
    Route("/posts/", ['GET'], "list published post", "Public"),
    Route("/posts/<pk>/", ['GET'], "get post using post slug", "Public"),
    Route("/posts/<pk>/", ['PATCH', 'POST', 'DELETE'],
          "create, update, delete post", "Writer"),
    Route("/posts/<slug>/submit/ ", ['POST', 'DELETE'],
          "Submit a post or delete a submission", "Writer"),
    Route("/posts/search/<searchTerm>/",
          ['GET'], "Search published post", "Public"),
    Route("/posts/subscribe/",
          ['GET'], "Subscribe to get newsletter when new post gets published", "User"),
    Route("/posts/top/", ['GET'], "Get top featured posts", "Public"),
    Route("/posts/writer/<writer_id>/", ['GET'], "Featured posts", "Public"),
    Route("/staff/applications/review/",
          ['GET'], "Writer applications yet to be reviewed", "Staff"),
    Route("/staff/applications/review/<approved>/",
          ['GET'], "Writer applications that has been approved", "Staff"),
    Route("/staff/review/<w_id>/", ['GET', 'PATCH'],
          "Get, approve or reject a writer application", "Staff"),
    Route("/upload/images/post/",
          ['POST'], "Upload a image for a post and get image url", "Writer"),
    Route("/upload/images/post/thumbnail/",
          ['POST'], "Upload a thumbnail for a post and get image url", "Writer"),
    Route("/upload/images/profile-pic/",
          ['POST'], "Upload a profile image", "User"),
    Route("/writer/<writer_name>/", ['GET'],
          "Get a writer's profile", "Public"),
    Route('/admin/', ['GET', 'POST'], "Admin panel", "Staff"),
    Route('/media/', ['GET'], "Media files", "Public"),
    Route('/static/', ['GET'], "Static files", "Public"),
]


def home_view(request):
    return render(request, 'home.html', {'routes': allRoutes})
