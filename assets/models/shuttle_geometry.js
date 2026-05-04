
// Procedural Space Shuttle Geometry Generator
// Can be included in the main HTML or loaded dynamically

function createSpaceShuttleGeometry() {
    const shuttleGroup = new THREE.Group();

    // Materials
    const whiteTileMat = new THREE.MeshStandardMaterial({ 
        color: 0xffffff, 
        roughness: 0.9, 
        metalness: 0.1,
        bumpScale: 0.02
    });
    
    const blackTileMat = new THREE.MeshStandardMaterial({ 
        color: 0x111111, 
        roughness: 0.9, 
        metalness: 0.1 
    });
    
    const engineMat = new THREE.MeshStandardMaterial({ 
        color: 0x333333, 
        roughness: 0.4, 
        metalness: 0.6 
    });

    const windowMat = new THREE.MeshStandardMaterial({
        color: 0x112244,
        roughness: 0.0,
        metalness: 0.9
    });

    // --- Fuselage ---
    // Main Cargo Bay Section (Box with rounded top/bottom or Cylinder?)
    // Real shuttle has a "double bubble" cross section somewhat, but flat bottom.
    // Let's use a Cylinder for the top and a Box for the bottom, merged?
    // Or just a Cylinder scaled.
    
    const fuselageGeo = new THREE.CylinderGeometry(2.8, 2.8, 18.3, 32);
    const fuselage = new THREE.Mesh(fuselageGeo, whiteTileMat);
    fuselage.rotation.x = Math.PI / 2;
    fuselage.position.z = 0; // Center of cargo bay at 0
    shuttleGroup.add(fuselage);

    // Flatten bottom of fuselage (visual hack: add a black box on bottom)
    const bellyGeo = new THREE.BoxGeometry(4.0, 1.0, 18.0);
    const belly = new THREE.Mesh(bellyGeo, blackTileMat);
    belly.position.y = -2.2;
    shuttleGroup.add(belly);

    // --- Nose Section ---
    // Complex shape: Tapered cylinder + cockpit windows
    const noseLength = 8.0;
    const noseGeo = new THREE.CylinderGeometry(0.5, 2.8, noseLength, 32);
    const nose = new THREE.Mesh(noseGeo, whiteTileMat);
    nose.rotation.x = Math.PI / 2;
    nose.position.z = 13.15; // 18.3/2 + 8.0/2
    shuttleGroup.add(nose);

    // Nose Cap (Black)
    const noseCapGeo = new THREE.SphereGeometry(0.5, 16, 16, 0, Math.PI*2, 0, Math.PI/2);
    const noseCap = new THREE.Mesh(noseCapGeo, blackTileMat);
    noseCap.rotation.x = Math.PI / 2;
    noseCap.position.z = 17.15;
    shuttleGroup.add(noseCap);

    // Cockpit Windows
    // Simple box intersecting the nose
    const cockpitGeo = new THREE.BoxGeometry(2.5, 1.0, 1.5);
    const cockpit = new THREE.Mesh(cockpitGeo, windowMat);
    cockpit.position.set(0, 1.8, 11.0);
    cockpit.rotation.x = -0.2;
    shuttleGroup.add(cockpit);

    // --- Wings ---
    // Double Delta
    const wingShape = new THREE.Shape();
    wingShape.moveTo(0, 0);
    wingShape.lineTo(2.0, 0); // Strake start
    wingShape.lineTo(6.0, -8.0); // Strake end / Wing start
    wingShape.lineTo(12.0, -12.0); // Wing tip
    wingShape.lineTo(12.0, -14.0); // Wing tip trailing
    wingShape.lineTo(2.5, -14.0); // Wing root trailing
    wingShape.lineTo(2.5, -16.0); // Body blend
    wingShape.lineTo(0, -16.0);
    
    const wingGeo = new THREE.ExtrudeGeometry(wingShape, { depth: 0.6, bevelEnabled: true, bevelSize: 0.1, bevelThickness: 0.1 });
    
    // Right Wing
    const rightWing = new THREE.Mesh(wingGeo, whiteTileMat);
    rightWing.rotation.x = Math.PI / 2;
    rightWing.rotation.y = Math.PI; // Flip to point back
    rightWing.position.set(1.5, -1.0, 8.0); // Adjust position
    shuttleGroup.add(rightWing);

    // Left Wing (Clone and Mirror)
    const leftWing = rightWing.clone();
    leftWing.scale.x = -1; // Mirror
    // Need to flip normals if scaling negatively? ThreeJS handles this usually but lighting might be weird.
    // Better to rotate?
    // If we scale X by -1, geometry is inside out?
    // Let's just rebuild geometry for left wing or rotate.
    // If we rotate 180 Z, it flips X and Y.
    // (x,y) -> (-x,-y).
    // Our shape is in XY plane.
    // Let's just use scale -1 x.
    shuttleGroup.add(leftWing);

    // Wing Leading Edges (Black)
    // Simplified: just paint the edges? Hard with simple mats.
    // We'll skip for now or add thin black strips.

    // --- Vertical Stabilizer ---
    const tailShape = new THREE.Shape();
    tailShape.moveTo(0, 0);
    tailShape.lineTo(0, 8.0);
    tailShape.lineTo(2.5, 8.0);
    tailShape.lineTo(6.0, 0);
    
    const tailGeo = new THREE.ExtrudeGeometry(tailShape, { depth: 0.8, bevelEnabled: true, bevelSize: 0.1, bevelThickness: 0.1 });
    const tail = new THREE.Mesh(tailGeo, whiteTileMat);
    tail.rotation.y = Math.PI / 2; // Align with Z
    tail.position.set(0, 2.5, -9.0);
    // Rotate to sweep back
    // Actually shape is drawn upright.
    // We need to rotate it so (0,0) is front-bottom.
    // Current shape: (0,0) -> (0,8) -> (2.5,8) -> (6,0).
    // This looks like a forward swept tail?
    // Real tail sweeps back.
    // Front-bottom (0,0). Front-top (3,8). Back-top (5,8). Back-bottom (9,0).
    // Let's redraw.
    const tailShape2 = new THREE.Shape();
    tailShape2.moveTo(0, 0); // Front bottom
    tailShape2.lineTo(4.0, 8.0); // Front top
    tailShape2.lineTo(6.5, 8.0); // Back top
    tailShape2.lineTo(9.0, 0); // Back bottom
    
    const tailGeo2 = new THREE.ExtrudeGeometry(tailShape2, { depth: 0.8, bevelEnabled: true, bevelSize: 0.1, bevelThickness: 0.1 });
    const tail2 = new THREE.Mesh(tailGeo2, whiteTileMat);
    tail2.rotation.y = -Math.PI / 2; // Align with Z, pointing back
    tail2.position.set(0.4, 2.5, -5.0); // Offset for thickness
    shuttleGroup.add(tail2);

    // --- OMS Pods ---
    const omsGeo = new THREE.BoxGeometry(3.0, 3.0, 5.0);
    const omsLeft = new THREE.Mesh(omsGeo, whiteTileMat);
    omsLeft.position.set(-2.5, 1.5, -10.0);
    shuttleGroup.add(omsLeft);
    
    const omsRight = new THREE.Mesh(omsGeo, whiteTileMat);
    omsRight.position.set(2.5, 1.5, -10.0);
    shuttleGroup.add(omsRight);

    // --- Main Engines (SSMEs) ---
    const engineGeo = new THREE.CylinderGeometry(1.2, 0.8, 2.5, 16);
    const engine1 = new THREE.Mesh(engineGeo, engineMat);
    engine1.rotation.x = Math.PI / 2;
    engine1.position.set(0, 2.0, -13.0); // Top
    shuttleGroup.add(engine1);

    const engine2 = new THREE.Mesh(engineGeo, engineMat);
    engine2.rotation.x = Math.PI / 2;
    engine2.position.set(1.8, -1.0, -13.0); // Right
    shuttleGroup.add(engine2);

    const engine3 = new THREE.Mesh(engineGeo, engineMat);
    engine3.rotation.x = Math.PI / 2;
    engine3.position.set(-1.8, -1.0, -13.0); // Left
    shuttleGroup.add(engine3);

    return shuttleGroup;
}

// Export for usage
window.createSpaceShuttleGeometry = createSpaceShuttleGeometry;
