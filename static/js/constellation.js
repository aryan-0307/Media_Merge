document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('constellation-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let width, height;
    function resize() {
        width = canvas.parentElement.clientWidth;
        height = canvas.parentElement.clientHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();
    
    const particles = [];
    const numParticles = 80;
    const maxDistance = 150;
    
    let mouse = { x: -1000, y: -1000 };
    canvas.parentElement.addEventListener('mousemove', function(e) {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });
    canvas.parentElement.addEventListener('mouseleave', function() {
        mouse.x = -1000;
        mouse.y = -1000;
    });
    
    for (let i = 0; i < numParticles; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: Math.random() * 2 + 1,
            isCobalt: Math.random() > 0.7
        });
    }
    
    function draw() {
        ctx.clearRect(0, 0, width, height);
        
        for (let i = 0; i < numParticles; i++) {
            let p = particles[i];
            
            let dxMouse = p.x - mouse.x;
            let dyMouse = p.y - mouse.y;
            let distMouse = Math.sqrt(dxMouse*dxMouse + dyMouse*dyMouse);
            if (distMouse < 100) {
                p.x += dxMouse * 0.02;
                p.y += dyMouse * 0.02;
            }
            
            p.x += p.vx;
            p.y += p.vy;
            
            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;
            
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = p.isCobalt ? 'rgba(26, 79, 219, 0.8)' : 'rgba(255, 255, 255, 0.8)';
            ctx.fill();
            
            for (let j = i + 1; j < numParticles; j++) {
                let p2 = particles[j];
                let dx = p.x - p2.x;
                let dy = p.y - p2.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                
                if (dist < maxDistance) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    let opacity = 1 - (dist / maxDistance);
                    let color = (p.isCobalt || p2.isCobalt) ? 'rgba(26, 79, 219, ' + (opacity * 0.5) + ')' : 'rgba(255, 255, 255, ' + (opacity * 0.3) + ')';
                    ctx.strokeStyle = color;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
            
            if (distMouse < maxDistance) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(mouse.x, mouse.y);
                let opacity = 1 - (distMouse / maxDistance);
                ctx.strokeStyle = p.isCobalt ? 'rgba(26, 79, 219, ' + (opacity * 0.5) + ')' : 'rgba(255, 255, 255, ' + (opacity * 0.3) + ')';
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
        
        requestAnimationFrame(draw);
    }
    
    draw();
});
