from Core.Option_values import get_instagram_data, get_facebook_data, get_youtube_data, get_blog_data, \
    get_pinterest_data, get_delete_data, get_deactivate_data, get_support_data, get_pwd_data, get_user_data, \
    set_instagram_data, set_facebook_data, set_youtube_data, set_pinterest_data, set_personal_blog_data, set_user_data, \
    set_pwd_data, set_deactivate_data, set_delete_data, get_base_data, set_base_data, get_company_pwd_data, \
    set_company_pwd_data, get_book_data, set_book_data, get_profile_pictures_sources, get_company_logo_data, \
    set_company_logo_data, set_delete_data_company, get_delete_data_company
from Core.admin.getter_setter.Administration import get_kpi_data, get_usermanaegemnt_data, get_d_data


def get_templates_getters_and_setters() -> dict:
    return {
        "profile": {
            "user": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/user.html",
                "getter": get_user_data,
                "setter": set_user_data
            },
            "pwd": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/pwd.html",
                "getter": get_pwd_data,
                "setter": set_pwd_data
            },
            "galery": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/galery.html",
                "getter": get_profile_pictures_sources
            },
            "support": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/faq.html",
                "getter": get_support_data
            },
            "cooperations": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/cooperations.html",
                "getter": get_deactivate_data,
                "setter": set_deactivate_data
            },
            "delete": {
                "template": "/preferences/subviews/subtopic_prefereces/profile/delete.html",
                "getter": get_delete_data,
                "setter": set_delete_data
            }
        },
        "channels": {
            "instagram": {
                "template": "/preferences/subviews/subtopic_prefereces/channels/instagram.html",
                "getter": get_instagram_data,
                "setter": set_instagram_data
            },
            "facebook": {
                "template": "/preferences/subviews/subtopic_prefereces/channels/facebook.html",
                "getter": get_facebook_data,
                "setter": set_facebook_data
            },
            "youtube": {
                "template": "/preferences/subviews/subtopic_prefereces/channels/youtube.html",
                "getter": get_youtube_data,
                "setter": set_youtube_data
            },
            "pinterest": {
                "template": "/preferences/subviews/subtopic_prefereces/channels/pinterest.html",
                "getter": get_pinterest_data,
                "setter": set_pinterest_data
            },
            "blog": {
                "template": "/preferences/subviews/subtopic_prefereces/channels/blog.html",
                "getter": get_blog_data,
                "setter": set_personal_blog_data
            }

        },
        "company": {
            "base": {
                "template": "/company_preferences/views/company_base.html",
                "getter": get_base_data,
                "setter": set_base_data
            },
            "pwd": {
                "template": "/company_preferences/views/company_access_pwd.html",
                "getter": get_company_pwd_data,
                "setter": set_company_pwd_data
            },
            "logo": {
                "template": "/company_preferences/views/company_logo.html",
                "getter": get_company_logo_data,
                "setter": set_company_logo_data
            },
            "book": {
                "template": "/company_preferences/views/company_book.html",
                "getter": get_book_data,
                "setter": set_book_data
            },
            "delete": {
                "template": "/company_preferences/views/delete.html",
                "getter": get_delete_data_company,
                "setter": set_delete_data_company
            }
        }
    }


def get_view_data_of_admin_view() -> dict:
    return {
        "kpis": {
            "getter": get_kpi_data,
            "template": "admin/logged_in/kpis/index.html",
        },
        "usermanagement": {
            "getter": get_usermanaegemnt_data,
            "template": "admin/logged_in/usermanagement/index.html"
        },
        "d": {
            "getter": get_d_data,
            "template": "admin/logged_in/d/index.html"
        }
    }
