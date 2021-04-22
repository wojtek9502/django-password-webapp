function get_polygon_center(polygon_locaton_array){
            var min_x = 180    //max lat
            var max_x = -180   //min lat
            var min_y = 90     //max lng
            var max_y = -90    //min lng
            for (var i = 0; i < polygon_locaton_array.length; i++) {

                if(polygon_locaton_array[i]['lat'] <  min_x){
                    min_x = polygon_locaton_array[i]['lat']
                }
                if(polygon_locaton_array[i]['lat'] >  max_x){
                    max_x = polygon_locaton_array[i]['lat']
                }

                if(polygon_locaton_array[i]['lng'] <  min_y){
                    min_y = polygon_locaton_array[i]['lng']
                }
                if(polygon_locaton_array[i]['lng'] >  max_y){
                    max_y = polygon_locaton_array[i]['lng']
                }
            }
            center_x = min_x + ((max_x - min_x) / 2);
            center_y = min_y + ((max_y - min_y) / 2)

            var center_xy = new Map()
            center_xy.set('center_lat', center_x)
            center_xy.set('center_lng', center_y)
            return center_xy
    }