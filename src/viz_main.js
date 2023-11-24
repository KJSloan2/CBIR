import * as THREE from 'three';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.119.1/examples/jsm/controls/OrbitControls.js';

const pointCloud = new THREE.Group();
const labelContainer = new THREE.Group(); // Container for labels
let scene, renderer, camera, raycaster, mouse;
let hoveredImage;
let currentFilterTag = null;

function loadCSV(filePath) {
    fetch(filePath)
        .then(response => response.text())
        .then(data => parseCSV(data))
        .catch(error => console.error('Error loading CSV:', error));
}

function parseCSV(csvData) {
    const uniqueLocationTags = new Set();
    const planeGeometry = new THREE.PlaneGeometry(3, 3);
    function makeInstance(texture, x, y, z, id, color,locationTag, year, month) {
        const planeMaterial = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
        const obj = new THREE.Mesh(planeGeometry, planeMaterial);
        obj.position.set(x, y, z);
        obj.userData.id = id;
        obj.userData.coords = [x, y, z];
        obj.userData.locationTag = locationTag;
        obj.userData.month = month;
        obj.userData.year = year;
        obj.userData.color = color;
        obj.userData.year = year;
        obj.rotation.x = Math.PI;
        obj.rotation.y = Math.PI;
        //obj.rotation.z = Math.PI;
        pointCloud.add(obj);
        return obj;
    }
    const lines = csvData.split('\n');
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const id = values[0];
        const x = parseFloat(values[1])*255;
        const y = parseFloat(values[2])*255;
        const z = parseFloat(values[3])*255;
        const r = parseFloat(values[4]) / 255;
        const g = parseFloat(values[6]) / 255;
        const b = parseFloat(values[5]) / 255;
        const locationTag = values[9];
        const year = values[10];
        const month = values[11];
        const color = new THREE.Color(r, g, b);


        uniqueLocationTags.add(locationTag);

        //const filePath = `../textures/${id}.jpg`;
        const filePath = `${id}.jpg`;
        const scale = 0.5;
        const loader = new THREE.TextureLoader();
        const texture = loader.load(filePath);
        makeInstance(texture, x, y, z, id, color, locationTag, year, month).scale.set(scale, scale, scale);
    }
    const filterControls = document.getElementById('filter-controls');
    uniqueLocationTags.forEach(tag => {
        const filterButton = document.createElement('button');
        filterButton.textContent = tag;
        filterButton.className = 'filter-button'; // Add the filter-button class
        filterButton.addEventListener('click', function() {
            filterByLocationTag(tag);
        });
        filterControls.appendChild(filterButton);
    });
        scene.add(pointCloud);
        scene.add(labelContainer);
}

/*function filterByLocationTag(tag) {
    // Hide all points
    pointCloud.children.forEach(point => {
        point.visible = false;
    });

    // Show points with the selected location tag
    pointCloud.children
        .filter(point => point.userData.locationTag === tag)
        .forEach(point => {
            point.visible = true;
        });
}*/

function filterByLocationTag(tag) {
    // If the same tag is clicked again, remove the filter
    if (tag === currentFilterTag) {
        currentFilterTag = null;
    } else {
        currentFilterTag = tag;
    }

    // Hide all points
    pointCloud.children.forEach(point => {
        point.visible = false;
    });

    // Show points with the selected location tag or show all if no filter
    if (currentFilterTag) {
        pointCloud.children
            .filter(point => point.userData.locationTag === currentFilterTag)
            .forEach(point => {
                point.visible = true;
            });
    } else {
        pointCloud.children.forEach(point => {
            point.visible = true;
        });
    }
}

function init() {
    scene = new THREE.Scene();
    const color = 0xFFFFFF;
    const light = new THREE.AmbientLight(0x404040, 3);
    scene.add(light);
    camera = new THREE.PerspectiveCamera(1000, window.innerWidth / window.innerHeight, 0.1, 500);
    camera.position.z = 50;
    camera.lookAt(new THREE.Vector3(80, 60, -11));
    renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    loadCSV('imageStats.csv');

    const controls = new OrbitControls(camera, renderer.domElement);
    
    controls.target.set(80, 60, -11);
    // Setup raycaster and mouse
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // Event listeners for mouseover and mouseout
    document.addEventListener('mousemove', onMouseMove, false);
    document.addEventListener('mouseout', onMouseOut, false);
    window.addEventListener( 'resize', onWindowResize );

}

function onMouseMove(event) {
    // Update the mouse position
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Raycast to find intersected objects
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(pointCloud.children, true);
    const enlargedImageContainer = document.getElementById('enlarged-image');
    if (intersects.length > 0 && intersects[0].object.userData) {
        // Get userData from the intersected object
        const { id, coords, color, locationTag, year, month } = intersects[0].object.userData;
        const filePath = `${id}.jpg`;
        enlargedImageContainer.innerHTML = `<img src="${filePath}" style="width: 100%; height: 100%;" />`;
        enlargedImageContainer.style.display = 'block';
        // Show tooltip with ID, coords, and color
        const tooltip = document.getElementById('tooltip');
        tooltip.innerHTML = `
            <strong>ID:</strong> ${id}<br>
            <strong>Coords:</strong> [${coords.join(', ')}]<br>
            <strong>location tag:</strong> [${locationTag}]<br>
            <strong>year:</strong> [${year}]<br>
            <strong>month:</strong> [${month}]<br>
            <strong>Color:</strong> ${color.getStyle()}
        `;
        tooltip.style.display = 'block';

    } else {
        // Hide tooltip if no intersection or missing userData
        document.getElementById('tooltip').style.display = 'none';
        enlargedImageContainer.style.display = 'none';

        /*pointCloud.children.forEach(point => {
            point.visible = true;
        });*/
    }
    /*console.log('Current Camera Settings:');
    console.log('Position:', camera.position);
    console.log('Rotation:', camera.rotation);
    console.log('Target:', camera.getWorldDirection(new THREE.Vector3()).add(camera.position));*/
}


function onMouseOut() {
    // Hide tooltip on mouseout
    document.getElementById('tooltip').style.display = 'none';
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

function animate() {
    requestAnimationFrame(animate);
    pointCloud.children.forEach(point => {
        //point.rotation.x += 0.01; // Rotate around X-axis
        //point.rotation.y += 0.02; // Rotate around Y-axis
    });
    labelContainer.rotation.copy(camera.rotation); // Make labels face the camera
    renderer.render(scene, camera);
}

init();
animate();
