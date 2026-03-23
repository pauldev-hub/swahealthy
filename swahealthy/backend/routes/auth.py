"""
Authentication routes — Google OAuth login/logout.
"""

from flask import Blueprint, render_template, session, redirect, url_for

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/google-login')
def google_login():
    from backend import google
    redirect_uri = url_for('auth.callback', _external=True).replace('127.0.0.1', 'localhost')
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/callback')
def callback():
    from backend import google
    from backend.models.helpers import upsert_user

    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    if user_info:
        user = upsert_user(user_info)
        session['user'] = user
    return redirect(url_for('main.index'))


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/debug-oauth')
def debug_oauth():
    """Debug route — shows first 20 chars of credentials. Remove before deploying."""
    import os
    cid = os.environ.get('GOOGLE_CLIENT_ID', 'NOT SET')
    csecret = os.environ.get('GOOGLE_CLIENT_SECRET', 'NOT SET')
    redirect_uri = url_for('auth.callback', _external=True).replace('127.0.0.1', 'localhost')
    return f"""
    <pre>
    GOOGLE_CLIENT_ID (first 20):   '{cid[:20]}...'
    Ends with correct suffix:       {cid.endswith('.apps.googleusercontent.com')}
    GOOGLE_CLIENT_SECRET present:   {bool(csecret and csecret != 'NOT SET')}
    OAUTHLIB_INSECURE_TRANSPORT:    {os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', 'not set')}
    Redirect URI Flask will use:    {redirect_uri}

    Checklist:
    [ ] Client ID ends with .apps.googleusercontent.com  --> {cid.endswith('.apps.googleusercontent.com')}
    [ ] Client Secret is present                         --> {bool(csecret)}
    [ ] OAUTHLIB_INSECURE_TRANSPORT=1 for localhost      --> {os.environ.get('OAUTHLIB_INSECURE_TRANSPORT') == '1'}
    [ ] Redirect URI matches Google Console              --> {redirect_uri}
         (Must add exactly this to Google Console!)
    </pre>
    """
