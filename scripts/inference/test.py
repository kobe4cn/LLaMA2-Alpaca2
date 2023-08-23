from gradio_client import Client

client = Client("https://3c47e83abc2060ed5c.gradio.live")
# client.view_api(return_format="dict")
result = client.predict(
				"test.json",	# str (filepath to JSON file) in 'parameter_1' Chatbot component
				512,	# int | float (numeric value between 0 and 4096) in 'Maximum New Token Length' Slider component
				0.9,	# int | float (numeric value between 0 and 1) in 'Top P' Slider component
				0.5,	# int | float (numeric value between 0 and 1) in 'Temperature' Slider component
				40,	# int | float (numeric value between 1 and 40) in 'Top K' Slider component
				True,	# bool in 'Do Sample' Checkbox component
				1.1,	# int | float (numeric value between 1.0 and 3.0) in 'Repetition Penalty' Slider component
				fn_index=1
)

print(result)
# job = client.submit(">>>><<<<中是用户对于某化妆品产品的使用感受评论内容，请判断该评论内容是正面还是负面评价，如果是积极的正面评价请回复正向评价，如果是消极的负面评价请给出判断依据，如果是无法判断请告知无法判断。>>>>今天来和大家分享这个欧莱雅黑胖子气垫，本人T区油，两颊干，偶尔状态不佳的时候鼻子还脱皮，冬季还好，可以做好保湿，夏季最头疼，再注意还是会出油。粉底液呢，比较厚重，所以选择了试下气垫，网上很多人推荐爱敬气垫，性价比高，但是我用了，遮瑕不好，而且特别容易脱妆，摘下口罩就特别明显。后来试了升级款的黑胖子，真心好。外包高级感，手感也好！质地轻薄，不油腻，不容易脱妆，早晨7.00上妆，办公室午休，起来后只是鼻翼两侧出点油，其他没有。还挺喜欢。比粉底液轻薄，而且方便！遮瑕力度也不错。是我喜欢的第一款气垫！<<<<", api_name="/predict")  # runs the prediction in a background thread
# job.result()

