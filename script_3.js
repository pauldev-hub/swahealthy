
(function(){
  var nav = document.querySelector('.navbar');
  if(!nav) return;
  var last = 0, delta = 8, navH = nav.offsetHeight;
  window.addEventListener('scroll', function(){
    var cur = window.scrollY;
    if(Math.abs(cur - last) < delta) return;
    if(cur > last && cur > navH) {
      nav.style.transform = 'translateY(-110%)';
    } else {
      nav.style.transform = 'translateY(0)';
    }
    last = cur;
  }, {passive: true});
})();

