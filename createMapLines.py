import sydneybuses
import random

COLOURS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000', '#008080', '#800080']
 
fo = open('mapLines.js', 'w')

for route in sydneybuses.sydneybuses.keys():
	colour = random.choice(COLOURS)
	print route, colour

	polyLineJS = 	"""var routePath = new google.maps.Polyline({
			path: ["""

	for path in sydneybuses.sydneybuses[route]:
		latlongJS = []

		latlongJS.append('new google.maps.LatLng(%s, %s), ' % (path['lat'], path['lon']))
		latlongJS = ', '.join(latlongJS)
		
		polyLineJS += latlongJS
		#polyLineJS = polyLineJS[:-2]

	polyLineJS+= """], 
			strokeColor: '%s',
			strokeOpacity: 1.0,
			strokeWeight: 2
			});
			routePath.setMap(map);
			""" % (colour)
			
	fo.write(polyLineJS)
fo.close()

