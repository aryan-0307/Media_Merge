document.addEventListener('DOMContentLoaded', function() {
    // Only run on non-touch devices
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const dot = document.createElement('div');
    dot.classList.add('custom-cursor-dot');
    document.body.appendChild(dot);

    const ring = document.createElement('div');
    ring.classList.add('custom-cursor-ring');
    document.body.appendChild(ring);

    let mouseX = -100;
    let mouseY = -100;
    let ringX = -100;
    let ringY = -100;

    window.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
        dot.style.transform = 'translate(calc(' + mouseX + 'px - 50%), calc(' + mouseY + 'px - 50%))';
    });

    function render() {
        ringX += (mouseX - ringX) * 0.2;
        ringY += (mouseY - ringY) * 0.2;
        ring.style.transform = 'translate(calc(' + ringX + 'px - 50%), calc(' + ringY + 'px - 50%))';
        requestAnimationFrame(render);
    }
    render();

    function addHoverListeners() {
        const interactables = document.querySelectorAll('a, button, .btn, .media-card, input, select, textarea, [role="button"]');
        interactables.forEach(function(el) {
            if (el.dataset.cursorBound) return;
            el.dataset.cursorBound = "true";
            el.addEventListener('mouseenter', function() {
                ring.classList.add('hovering');
                dot.style.opacity = '0';
            });
            el.addEventListener('mouseleave', function() {
                ring.classList.remove('hovering');
                dot.style.opacity = '1';
            });
        });
    }

    addHoverListeners();

    // Re-bind on DOM changes (for dynamic content)
    const observer = new MutationObserver(addHoverListeners);
    observer.observe(document.body, { childList: true, subtree: true });
});
