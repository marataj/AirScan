scanning_form = document.getElementById('scanning_form')
area_field=document.getElementById('scanning_area')
map_info_field=document.getElementById('map_info')

document.getElementById('submit_scanner').onclick = () => 
{
    const drawnArrays = window.frames["0"].drawnItems._layers;
    areas=[]
    for (const [key, value] of Object.entries(drawnArrays)) {
        areas.push({NE: value._bounds._northEast, SW: value._bounds._southWest})
      }
      area_field.value=JSON.stringify(areas)
      getMapInfo()
      scanning_form.submit()
}

function getMapInfo() {
  center=window.frames["0"].drawnItems._map.getCenter()
  zoom_val=window.frames["0"].drawnItems._map.getZoom()
  console.log(center)
  console.log(zoom_val)
  map_info={
    lat: center.lat,
    lng: center.lng,
    zoom: zoom_val
  }
  map_info_field.value=JSON.stringify(map_info)
}

function change_map_center(lon, lat, zoom) {
  map=window.frames["0"].drawnItems._map
  map.setView([lon,lat], zoom)
}

