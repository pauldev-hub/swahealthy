
        (function () {
            var showSplash = true;
            try {
                showSplash = sessionStorage.getItem('swahealthy_boot_splash_seen') !== '1';
            } catch (err) {
                showSplash = true;
            }
            document.documentElement.classList.toggle('app-splash-boot', showSplash);
            window.__showSwahealthySplash = showSplash;
        })();
    
