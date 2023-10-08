let noise = new SimplexNoise();
let vizInit = function (){
    let file = document.getElementById("thefile");
    let audio = document.getElementById("audio");
    let fileLabel = document.querySelector("label.file");
  
    document.onload = function(e){
        console.log(e);
        audio.play();
        play();
    }

    file.onchange = function(){
        fileLabel.classList.add('normal');
        audio.classList.add('active');
        let files = this.files;
        
        audio.src = URL.createObjectURL(files[0]);
        audio.classList.remove('active')
        audio.classList.add('hidden')
        audio.load();
        audio.play();
        play();
    }
  
    function play() {
        let context = new AudioContext();
        let src = context.createMediaElementSource(audio);
        let analyser = context.createAnalyser();
        src.connect(analyser);
        analyser.connect(context.destination);
        analyser.fftSize = 512;

        let bufferLength = analyser.frequencyBinCount;
        let dataArray = new Uint8Array(bufferLength);

        const textureLoader = new THREE.TextureLoader();

        let scene = new THREE.Scene();
        let group = new THREE.Group();
        let camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);

        camera.position.set(0,100,200);
        camera.lookAt(scene.position);
        scene.add(camera);

        let cameraDistance = 170;
        let cameraAngle = 0;

        let renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);

        let planeGeometry = new THREE.PlaneGeometry(1500, 1500, 20, 20);
        let planeMaterial = new THREE.MeshLambertMaterial({
            color: 0x6904ce,
            side: THREE.DoubleSide,
            wireframe: true
        });

        let texture_back = textureLoader.load('plane.jpg');

        let backPlaneMaterial = new THREE.MeshLambertMaterial({
            map: texture_back,
            side: THREE.DoubleSide,
            wireframe: false
        })
    
        let upPlane = new THREE.Mesh(planeGeometry, planeMaterial);
        upPlane.rotation.x = -0.5 * Math.PI;
        upPlane.position.set(0, 150, 0);
        group.add(upPlane);
    
        let downPlane = new THREE.Mesh(planeGeometry, planeMaterial);
        downPlane.rotation.x = -0.5 * Math.PI;
        downPlane.position.set(0, -150, 0);
        group.add(downPlane);

        var planeSize = 1000; // Adjust the size of the planes as needed
        var planeHeight = 1000; // Adjust the height of the planes as needed

        // Define the positions and rotations for the planes to create a box
        var planePositions = [
            { x: 0, y: 0, z: -planeSize / 2 }, // Back plane
            { x: 0, y: 0, z: planeSize / 2 }, // Front plane
            { x: -planeSize / 2, y: 0, z: 0 }, // Left plane
            { x: planeSize / 2, y: 0, z: 0 }, // Right plane
        ];
        var planeRotations = [
            { x: 0, y: 0, z: 0 }, // Back plane
            { x: 0, y: Math.PI, z: 0 }, // Front plane
            { x: 0, y: -Math.PI / 2, z: 0 }, // Left plane
            { x: 0, y: Math.PI / 2, z: 0 }, // Right plane
        ];

        // Create the planes
        for (var i = 0; i < 4; i++) {
            var backPlane = new THREE.Mesh(
                new THREE.PlaneGeometry(planeSize, planeHeight),
                backPlaneMaterial
            );
            backPlane.position.set(planePositions[i].x, planePositions[i].y, planePositions[i].z);
            backPlane.rotation.set(planeRotations[i].x, planeRotations[i].y, planeRotations[i].z);
            group.add(backPlane);
        }
        
        let icosahedronGeometry = new THREE.IcosahedronGeometry(10, 4);
        let lambertMaterial = new THREE.MeshLambertMaterial({
            color: 0xff00ee,
            wireframe: true
        });

        let sphere = new THREE.Mesh(icosahedronGeometry, lambertMaterial);
        sphere.position.set(0, 0, 0);
        group.add(sphere);

        const texture_1 = textureLoader.load('texture.jpg');
        const texture_2 = textureLoader.load('texture2.jpg');
        const texture_3 = textureLoader.load('texture3.jpg');

        let decorationMaterial_1 = new THREE.MeshLambertMaterial({
            map: texture_1,
            wireframe: false
        })

        let decorationMaterial_2 = new THREE.MeshLambertMaterial({
            map: texture_2,
            wireframe: false
        })

        let decorationMaterial_3 = new THREE.MeshLambertMaterial({
            map: texture_3,
            wireframe: false
        })

        let decorationSphere1 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_1);
        let decorationSphere2 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_2);
        let decorationSphere3 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_3);
        let decorationSphere4 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_2);
        let decorationSphere5 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_1);
        let decorationSphere6 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_3);
        let decorationSphere7 = new THREE.Mesh(icosahedronGeometry, decorationMaterial_2);

        decorationSphere1.position.set(70, 90, -150);
        decorationSphere2.position.set(-70, 130, 120);
        decorationSphere3.position.set(50, -85, 190);
        decorationSphere4.position.set(-100, -90, 80);
        decorationSphere5.position.set(100, -70, 100);
        decorationSphere6.position.set(-80, -90, -150);
        decorationSphere7.position.set(-95, 120, -100);

        scene.add(decorationSphere1);
        scene.add(decorationSphere2);
        scene.add(decorationSphere3);
        scene.add(decorationSphere4);
        scene.add(decorationSphere5);
        scene.add(decorationSphere6);
        scene.add(decorationSphere7);

        let ambientLight = new THREE.AmbientLight(0xffffff);
        scene.add(ambientLight);

        let spotLight = new THREE.SpotLight(0xffffff);
        spotLight.intensity = 0.9;
        spotLight.position.set(0, 100, 0);
        spotLight.lookAt(sphere);
        spotLight.castShadow = true;
        scene.add(spotLight);

        scene.add(group);

        document.getElementById('out').appendChild(renderer.domElement);

        window.addEventListener('resize', onWindowResize, false);

        render();

        function render() {
        analyser.getByteFrequencyData(dataArray);

            let lowerHalfArray = dataArray.slice(0, (dataArray.length/2) - 1);
            let upperHalfArray = dataArray.slice((dataArray.length/2) - 1, dataArray.length - 1);

            let overallAvg = avg(dataArray);
            let lowerMax = max(lowerHalfArray);
            let lowerAvg = avg(lowerHalfArray);
            let upperMax = max(upperHalfArray);
            let upperAvg = avg(upperHalfArray);

            let lowerMaxFr = lowerMax / lowerHalfArray.length;
            let lowerAvgFr = lowerAvg / lowerHalfArray.length;
            let upperMaxFr = upperMax / upperHalfArray.length;
            let upperAvgFr = upperAvg / upperHalfArray.length;

            makeRoughGround(upPlane, modulate(0, 0, 1, 0.5, 4));
            makeRoughGround(downPlane, modulate(0, 0, 1, 0.5, 4));
            
            makeRoughBall(sphere, modulate(Math.pow(lowerMaxFr, 0.8), 0, 1, 0, 8), modulate(upperAvgFr, 0, 1, 0, 4));

            // Calculate the rotation angle for the ball to move in a circle
            let angle = performance.now() * 0.0008;
            let radius = 120; // Adjust the radius as needed

            // Calculate the new position of the ball in a circle
            let ballX = Math.cos(angle) * radius;
            let ballZ = Math.sin(angle) * radius;
            sphere.position.set(ballX, 0, ballZ);

            let cameraX = sphere.position.x + cameraDistance * Math.cos(cameraAngle);
            let cameraY = sphere.position.y;
            let cameraZ = sphere.position.z + cameraDistance * Math.sin(cameraAngle);

            camera.position.set(cameraX, cameraY, cameraZ);

            camera.lookAt(sphere.position);

            cameraAngle += -0.01; 

            //group.rotation.y += 0.005;
            renderer.render(scene, camera);
            requestAnimationFrame(render);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function makeRoughBall(mesh, bassFr, treFr) {
            mesh.geometry.vertices.forEach(function (vertex, i) {
                let offset = mesh.geometry.parameters.radius;
                let amp = 10;
                let time = window.performance.now();
                vertex.normalize();
                let rf = 0.00001;
                let distance = (offset + bassFr ) + noise.noise3D(vertex.x + time *rf*7, vertex.y +  time*rf*8, vertex.z + time*rf*9) * amp * treFr;
                vertex.multiplyScalar(distance);
            });
            mesh.geometry.verticesNeedUpdate = true;
            mesh.geometry.normalsNeedUpdate = true;
            mesh.geometry.computeVertexNormals();
            mesh.geometry.computeFaceNormals();
        }

        function makeRoughGround(mesh, distortionFr) {
            mesh.geometry.vertices.forEach(function (vertex, i) {
                let amp = 10;
                let time = Date.now();
                let distance = (noise.noise2D(vertex.x + time * 0.0003, vertex.y + time * 0.0001) + 0) * distortionFr * amp;
                vertex.z = distance;
            });
            mesh.geometry.verticesNeedUpdate = true;
            mesh.geometry.normalsNeedUpdate = true;
            mesh.geometry.computeVertexNormals();
            mesh.geometry.computeFaceNormals();
        }

        audio.play();
    }
}

window.onload = vizInit();

document.body.addEventListener('touchend', function(ev) { context.resume(); });

function fractionate(val, minVal, maxVal) {
    return (val - minVal)/(maxVal - minVal);
}

function modulate(val, minVal, maxVal, outMin, outMax) {
    let fr = fractionate(val, minVal, maxVal);
    let delta = outMax - outMin;
    return outMin + (fr * delta);
}

function avg(arr){
    let total = arr.reduce(function(sum, b) { return sum + b; });
    return (total / arr.length);
}

function max(arr){
    return arr.reduce(function(a, b){ return Math.max(a, b); })
}