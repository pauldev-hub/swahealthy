
        (function () {
            var splash = document.getElementById('app-splash');
            if (!splash) return;
            if (!window.__showSwahealthySplash) {
                splash.hidden = true;
                return;
            }
            document.body.classList.add('splash-active');
            splash.style.opacity = '1';
            splash.style.visibility = 'visible';
        })();
    
