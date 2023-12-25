
# toio
toioのサイズは24x24
実寸32㎜
32/24=1.333333

座標1point=1.3333mm

# 方向
|方向|angle|
|-|-|
|上|0|
|右|90|
|下|180|
|左|270|

# 座標

座標はangle=0の時
|panel|x_max|x_min|y_max|y_min|
|  -  |  -  |  -  |  -  |  -  |
|    0|    7|   33|   64|   38|
|    1|   35|   63|   64|   38|
|    2|   64|   89|   65|   37|
|    3|   92|  120|   64|   37|
|    4|    6|   33|   36|    8|
|    5|   34|   63|   36|    9|
|    6|   64|   90|   36|    9|
|    7|   92|  119|   36|    9|  
|    8|    6|   32|    9|  -19|
|    9|   34|   62|    8|  -20|
|   10|  -79|  -53|    7|  -19|
|   11| -108|  -80|    7|  -19|
|   12|    6|   33|  -21|  -48|
|   13|   35|   61|  -21|  -49|
|   14|  -78|  -53|  -22|  -48|


|panel|center_x|center_y|
|  -  |   -    |   -    |
|    0|      11|      43|
|    1|      41|      43|
|    2|      70|      43|
|    3|      99|      43|
|    4|      12|      14|
|    5|      41|      14|
|    6|      70|      15|
|    7|      98|      14|
|    8|      11|     -14|
|    9|      40|     -14|
|   10|     -73|     -14|
|   11|    -103|     -14|
|   12|      11|     -43|
|   13|      40|     -42|
|   14|     -72|     -42|


上ゲート
x:panel_center_x - 3 < x < panel_center_x + 3 
y:panel_center_y + 18 < x < panel_center_y  + 20

下ゲート
x:panel_center_x - 3 < x < panel_center_x + 3 
y:panel_center_y - 20 < x < panel_center_y  - 18

右ゲート
x:panel_center_X + 18 < x < panerl_center_x + 20
y:panel_center_y - 3 < y panel_center_y + 3

左ゲート
x:panel_center_X - 20 < x < panerl_center_x - 18
y:panel_center_y - 3 < y panel_center_y + 3