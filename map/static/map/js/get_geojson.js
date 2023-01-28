document.getElementById('checkCoords').onclick = () => 
{
    const drawnArrays = window.frames["0"].drawnItems._layers;
    arreas=[]
    for (const [key, value] of Object.entries(drawnArrays)) {
        arreas.push({NEcoord: value._bounds._northEast, SWcoord: value._bounds._southWest})
        var NEcoord=value._bounds._northEast
        var SWcoord=value._bounds._southWest
      }
      console.log(arreas)
}