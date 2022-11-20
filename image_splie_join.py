import cv2

target_image = 'width1.png'

raw_img = cv2.imread(target_image, cv2.IMREAD_UNCHANGED)
dimensions = raw_img.shape
height = raw_img.shape[0]
width = raw_img.shape[1]

##원본이미지 crop to even pixels for divide
if height%2 == 1:
    new_height = height-1
else:
    new_height = height
if width%2 == 1:
    new_width = width-1
else:
    new_width = width

if (new_height==height)&(new_width==width):
    crop_img = raw_img
else:
    crop_img = raw_img[0:new_height,0:new_width]

#cell -- 22만 pixels maximum 최대 가로 1000 할 예정 for 1000*220
#cell 정보 get
#가로
if new_width < 1000:
    cell_width = new_width
    num_width = 1
else:
    cell_width = new_width / 2
    num_width = 2
    if cell_width > 1000:
        cell_width = new_width / 4
        num_width = 4
        if cell_width >1000:
            cell_width = new_width / 8
            num_width = 8
            if cell_width > 1000:
                cell_width = new_width / 16
                num_width = 16
                if cell_width > 1000:
                    cell_width = new_width / 32
                    num_width = 32
print(str(cell_width) + '<--만약 이 수가 1000보다 클 경우, cuda out of memory나올것임. ')

#세로
cell_height = 220
if new_height < cell_height:
    last_cell_height = new_height
    num_height = 1
else:
    num_height = new_height//cell_height + 1
    last_cell_height = new_height - ((num_height-1)*cell_height)
#make integer -- not float
num_height = int(num_height)
last_cell_height = int(last_cell_height)
num_width = int(num_width)
cell_width = int(cell_width)

##divede image
for i in range(num_width):
    for j in range(num_height):
        if j != num_height-1: #높이 = 220
            globals()['crop_img_{}_{}'.format(i,j)] = raw_img[j*cell_height:(j+1)*cell_height,i*cell_width:(i+1)*cell_width]
        else:##높이 =  last_cell_height
            globals()['crop_img_{}_{}'.format(i,j)] = raw_img[j*cell_height:j*cell_height+last_cell_height,i*cell_width:(i+1)*cell_width]


##save images ---crop_img_width_height(가로_세로)
#저장 전 삭제기능 추가 필요.
for i in range(num_width):
    for j in range(num_height):
        divided_img = globals()['crop_img_{}_{}'.format(i,j)]
        cv2.imwrite('./temp_folder/crop_img_{}_{}.png'.format(i,j),divided_img)
print('save fin')


##join images(원본 이미지.)-----------------------------------------------------------------------
# if (num_width==0) & (num_height==0):
#     re_join_img = raw_img
# elif (num_width==0) & (num_height>0):
#     for j in range(num_height):
#         if j == 0:
#             temp_merge_j = crop_img_0_0
#         else:
#             temp_merge_j = cv2.vconcat([temp_merge_j, globals()['crop_img_0_{}'.format(j)]])
#     re_join_img = temp_merge_j
# elif (num_width>0) & (num_height==0):##왜인지 2픽셀이 주는데? -- 아마 33~~코드에서 2면 1픽셀 감소 4면 2픽셀 감소 8면 4픽셀감소...인듯
#     for i in range(num_width):
#         if i == 0:
#             temp_merge_i = crop_img_0_0
#         else:
#             temp_merge_i = cv2.hconcat([temp_merge_j, globals()['crop_img_{}_0'.format(i)]])
#     re_join_img = temp_merge_i
# else:#i>0,j>0
#     for i in range(num_width):#num_width
#         for j in range(num_height):
#             if j == 0:
#                 temp_merge_j = globals()['crop_img_{}_0'.format(i)]
#             else:
#                 temp_merge_j = cv2.vconcat([temp_merge_j, globals()['crop_img_{}_{}'.format(i,j)]])
#         globals()['crop_img_{}'.format(i)] = temp_merge_j
#         if i == 0:
#             temp_merge_i = crop_img_0
#         else:
#             temp_merge_i = cv2.hconcat([temp_merge_i, globals()['crop_img_{}'.format(i)]])
#     re_join_img = temp_merge_i

##join images(처리된 이미지.)-----------------------------------------------------------------------
#png 여야함.
#위에 save전까지 선행 실행 필요.
if (num_width==0) & (num_height==0):
    re_join_img = cv2.imread('./temp_folder/crop_img_0_0_result.png', cv2.IMREAD_UNCHANGED)
elif (num_width==0) & (num_height>0):
    for load_img in range(num_height):##새로운 이미지 불러오기
        globals()['crop_img_0_{}_result'.format(load_img)] = cv2.imread('./temp_folder/crop_img_0_{}_result.png'.format(load_img), cv2.IMREAD_UNCHANGED)
    for j in range(num_height):
        if j == 0:
            temp_merge_j = cv2.imread('./temp_folder/crop_img_0_0_result.png', cv2.IMREAD_UNCHANGED)
        else:
            temp_merge_j = cv2.vconcat([temp_merge_j, globals()['crop_img_0_{}_result'.format(j)]])
    re_join_img = temp_merge_j
elif (num_width>0) & (num_height==0):##왜인지 2픽셀이 주는데? -- 아마 33~~코드에서 2면 1픽셀 감소 4면 2픽셀 감소 8면 4픽셀감소...인듯
    for load_img in range(num_width):##새로운 이미지 불러오기
            globals()['crop_img_{}_0_result'.format(load_img)] = cv2.imread('./temp_folder/crop_img_{}_0_result.png'.format(load_img), cv2.IMREAD_UNCHANGED)
    for i in range(num_width):
        if i == 0:
            temp_merge_i = cv2.imread('./temp_folder/crop_img_0_0_result.png', cv2.IMREAD_UNCHANGED)
        else:
            temp_merge_i = cv2.hconcat([temp_merge_i, globals()['crop_img_{}_0_result'.format(i)]])
    re_join_img = temp_merge_i
else:#i>0,j>0
    #새 이미지 불러오기
    for load_img_i in range(num_width):
        for load_img_j in range(num_height):
            globals()['crop_img_{}_{}_result'.format(load_img_i,load_img_j)] = cv2.imread('./temp_folder/crop_img_{}_{}_result.png'.format(load_img_i,load_img_j), cv2.IMREAD_UNCHANGED)
    print('불러오기')
    for i in range(num_width):#num_width
        for j in range(num_height):
            if j == 0:
                temp_merge_j = globals()['crop_img_{}_0_result'.format(i)]
            else:
                temp_merge_j = cv2.vconcat([temp_merge_j, globals()['crop_img_{}_{}_result'.format(i,j)]])
        globals()['crop_img_{}_result'.format(i)] = temp_merge_j
        if i == 0:
            temp_merge_i = crop_img_0_result#이거 오류 아님!
        else:
            temp_merge_i = cv2.hconcat([temp_merge_i, globals()['crop_img_{}_result'.format(i)]])
    re_join_img = temp_merge_i

cv2.imwrite('./result/'+str(target_image)+'_result.png',re_join_img)


small_img = cv2.resize(re_join_img, dsize=(0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
cv2.imwrite('./result/'+str(target_image)+'_result_small.png',small_img)



print("FINFINFINFINFIN")