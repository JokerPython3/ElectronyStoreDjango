document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('[data-toggle="pw"]').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      const target = document.querySelector(btn.getAttribute('data-target'));
      if(!target) return;
      if(target.type === 'password'){ target.type = 'text'; btn.textContent = btn.getAttribute('data-hide-text') || 'Hide'; }
      else { target.type = 'password'; btn.textContent = btn.getAttribute('data-show-text') || 'Show'; }
      target.focus();
    });
  });
  document.querySelectorAll('form[data-validate="true"]').forEach(function(form){
    form.addEventListener('submit', function(e){
      const required = form.querySelectorAll('[required]');
      let ok = true;
      required.forEach(function(inp){
        if(!inp.value.trim()){
          ok = false;
          inp.classList.add('invalid');
        } else {
          inp.classList.remove('invalid');
        }
      });
      if(!ok){
        e.preventDefault();
        form.animate([{transform:'translateX(-6px)'},{transform:'translateX(6px)'},{transform:'translateX(0)'}],{duration:260});
      }
    });
  });
});