# ModelBox-Solutions

## Solution列表

|解决方案名称|功能描述|输入data|输入meta|输出data|输入meta|
|-|-|-|-|-|-|
|手势识别|检测图片中的手的位置，然后识别手指的关键点。|图片文件流。|-|检测后图片，若检测到手，则画出手的框与手指连线；若未检测到手，则为原图。|width：图片宽度。 <br> height：图片高度。<br>channel：图片通道数。<br>pix_fmt：图片格式<br>has_hand：值判断是否有检测到手，True为检测到有手，False为未检测到手。为True才会有bboxes与hand_pose参数。<br>bboxes：检测到手的box坐标。<br>hand_pose：检测到手指位置坐标，每只手5根手指，每根手指3个关键点坐标。|
