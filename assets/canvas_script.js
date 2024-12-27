document.addEventListener("DOMContentLoaded", function () {
    setTimeout(()=>{
        // 600 x 100
        yc = 40;
        xs = 70
        xe = 530
        xc = 300
        console.log("Hello")
        const canvas = document.getElementById("myCanvas");
        console.log(canvas)
        const ctx = canvas.getContext("2d");

        // Draw a green triangle
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.moveTo(xc, yc);
        ctx.lineTo(xc+10, yc+20);
        ctx.lineTo(xc-10, yc+20);
        ctx.closePath();
        ctx.fill();

        // Define a new path
        ctx.beginPath();
        ctx.moveTo(xs, yc);
        ctx.lineTo(xe, yc);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(xs, yc-10);
        ctx.lineTo(xs, yc+10);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(xe, yc-10);
        ctx.lineTo(xe, yc+10);
        ctx.stroke();
        

        // Add text
        ctx.fillStyle = "black";
        ctx.font = "20px Verdana";
        ctx.fillText("954,- DKK", xc-45, yc+50);

        // Add text
        ctx.fillStyle = "black";
        ctx.font = "20px Verdana";
        ctx.fillText("902,-", xs-20, yc+50);

        // Add text
        ctx.fillStyle = "black";
        ctx.font = "20px Verdana";
        ctx.fillText("Lower bound", xs-60, yc-20);

        // Add text
        ctx.fillStyle = "black";
        ctx.font = "20px Verdana";
        ctx.fillText("984,-", xe-20, yc+50);

        // Add text
        ctx.fillStyle = "black";
        ctx.font = "20px Verdana";
        ctx.fillText("Upper bound", xe-70, yc-20);

        btn = document.getElementById('predict-button')
        btn.addEventListener('click', ()=>{
            elem = document.getElementById('canvas-container')
            elem.style.display = 'flex'
            console.log('display!!')
        })
    }, 500)

    
});
