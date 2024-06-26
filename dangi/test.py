import requests

# 업로드할 이미지 파일 경로
image_file = 'C:/Users/Playdata/Downloads/gg.JPG'

# POST 요청 보낼 엔드포인트 URL
url = 'http://127.0.0.1:8000/diet/record/image/'

# 이미지 파일 열기
with open(image_file, 'rb') as file:
    # 파일을 dictionary 형태로 준비 (key는 'image')
    files = {'img': (image_file, file, 'image/jpeg')}  # 파일 타입에 따라 적절히 수정

    # POST 요청 보내기 (multipart/form-data 형식)
    response = requests.post(url, files=files)
    print(response)
# 요청 결과 확인
if response.status_code == 200:
    print('이미지 업로드 성공!')
else:
    print(f'이미지 업로드 실패 - 응답 코드: {response.status_code}')

print(response.json())