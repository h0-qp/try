import requests,re,random,wget,yt_dlp,os,time
from pyrogram import Client , filters ,idle,enums
from user_agent import generate_user_agent

from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from pyrogram.types import InlineKeyboardMarkup as km, InlineKeyboardButton as btn

def stm(seconds):
	return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

def media(url):
	headers = {
		'authority': 'dotsave.app',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://dotsave.app',
		'referer': 'https://dotsave.app/',
		'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'same-origin',
		'user-agent': generate_user_agent()
}
	data = {
		'url': url,
		'lang': "en",
		'type': 'redirect'
}
	response = requests.post("https://dotsave.app/",headers=headers,data=data)
	#if response.json()["status"] == "ok":
	return response.text


def download_video(url, save_path,id):
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		with open(save_path, "wb") as video_file:
			for chunk in response.iter_content(chunk_size=1024 * 1024):
				if chunk:
					video_file.write(chunk)
			return True

me_ch = [ 
	[
		btn(text="الاحصائيات",callback_data="stats"),
		btn(text="اذاعة",callback_data="adaa")
	]
]
btns = km(me_ch)

what = {
	"adaa": "False",
}
mis = {
}

token = "5578804926:AAGNxODMKLiLy94OwkTyljGLXfYxk_CucvQ"  #توكنك
username = "@cn_world"  #يوزر قناك بعد @
dev = int("1160471152") #ايدي حسابك

in_msg = """
دخل شخص جديد للبوت الخاص بك.

اسمه: {}
ايديه: {}
معرفه: @{}

عدد اعضاء البوت الان {} عضو
"""
try:
	open("members.txt","r").read()
except Exception as error:
	print(error)
	open("members.txt","a").write("")

bot = Client("bot",
	api_id = 12124468, #ايبي ايدي بدون " "
	api_hash = "d672090b923c0789ef03c50740990c42", #ايبي هاش
	bot_token = token
	)

bot.start()

@bot.on_message(filters.command("start") & filters.private)
def welcome(bot,message):
	mention = message.from_user.mention
	name = message.from_user.first_name
	id = message.from_user.id
	if message.from_user.id != dev:
		members = open("members.txt","r")
		if str(message.from_user.id) not in str(members.read()):
			open("members.txt","a").write(f"{message.from_user.id}\n")
			number = 0
			for i in open("members.txt","r").readlines():
				number += 1
			bot.send_message(dev,in_msg.format(message.from_user.first_name,message.from_user.id,message.from_user.username,number))
		else:
			pass
		message.reply(f'''- مرحبا بك {mention}
	- في بوت تحميل من الانستكرام 
	
للتحميل ارسل الرابط فقط.''')
	else:
		message.reply("""
مرحبا بك سيدي في بوتك اختر ادناه...""",reply_markup=btns)
		message.reply(f'''- مرحبا بك {mention}
	- في بوت تحميل من الانستكرام 
	
للتحميل ارسل الرابط فقط.''')
@bot.on_message(filters.regex("^(http|https)://(www.|)instagram.com") & filters.private)
async def instagram(bot,message):
	print("instagram")
	link = message.text
	chat_id = message.chat.id
	if what["adaa"] == "True" and message.from_user.id == dev:
		done = 0
		users = open("members.txt","r").readlines()
		for user in users:
			try:
				await message.copy(user,chat_id)
				done += 1
			except:
				continue
		await messag.reply(f"تم ارسال الاذاعة الى {done} من الاعضاء")
		what["adaa"] = "False"
		return
	if "/p/" in link or "/reel/" in link:
		headers = {
			'authority': 'reelsaver.net',
			'accept': '*/*',
			'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin': 'https://reelsaver.net',
			'referer': 'https://reelsaver.net/download-reel-instagram',
			'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
			'sec-ch-ua-mobile': '?1',
			'sec-ch-ua-platform': '"Android"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'user-agent': generate_user_agent(),
			'x-requested-with': 'XMLHttpRequest'
		}
		data = {
			'via': 'form',
			'ref': 'download-reel-instagram',
			'url': link,
		}
		response = requests.post('https://reelsaver.net/api/instagram',headers=headers,data=data).json()
		#print(response)
		No = response['success']
		if No == False:
			await message.reply('<i>خطأ تأكد من الرابط ..</i>')
		else:
			await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
			#user = response['data']['user']['username']
			media = []
			for video in response["data"]['medias']:
				if len(media) >= 10:
					await message.reply_media_group(media)
					media.clear()
					continue
				video = video["src"]
				if ".mp4" in video:
					media.append(InputMediaVideo(video,caption=f"{username}"))
				else:
					media.append(InputMediaPhoto(video,caption=f"{username}"))
			await message.reply_media_group(media)
			media.clear()
	elif "/s/" in link:
		headers = {
			'authority': 'reelsaver.net',
			'accept': '*/*',
			'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin': 'https://reelsaver.net',
			'referer': 'https://reelsaver.net/download-highlights-instagram',
			'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
			'sec-ch-ua-mobile': '?1',
			'sec-ch-ua-platform': '"Android"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'user-agent': generate_user_agent(),
			'x-requested-with': 'XMLHttpRequest'
		}
		data = {
			'via': 'form',
			'ref': 'download-highlights-instagram',
			'url': link,
		}
		response = requests.post('https://reelsaver.net/api/instagram',headers=headers,data=data).json()
		No = response['success']
		if No == False:
			await message.reply('<i>خطأ تأكد من الرابط ..</i>')
		else:
			await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
			#user = response['data']['user']['username']
			media = []
			for video in response["data"]['medias']:
				if len(media) >= 10:
					await message.reply_media_group(media)
					media.clear()
					continue
				video = video["src"]
				if ".mp4" in video:
					media.append(InputMediaVideo(video,caption=f"{username}"))
				else:
					media.append(InputMediaPhoto(video,caption=f"{username}"))
			await message.reply_media_group(media)
			media.clear()
	else:
		headers = {
			'authority': 'reelsaver.net',
			'accept': '*/*',
			'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin': 'https://reelsaver.net',
			'referer': 'https://reelsaver.net/download-story-instagram',
			'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
			'sec-ch-ua-mobile': '?1',
			'sec-ch-ua-platform': '"Android"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'user-agent': generate_user_agent(),
			'x-requested-with': 'XMLHttpRequest'
		}
		data = {
			'via': 'form',
			'ref': 'download-story-instagram',
			'url': link,
		}
		response = requests.post('https://reelsaver.net/api/instagram',headers=headers,data=data).json()
		No = response['success']
		if No == False:
			await message.reply('<i>خطأ تأكد من الرابط ..</i>')
		else:
			await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
			media = []
			#user = response['data']['user']['username']
			for video in response["data"]['medias']:
				if len(media) >= 10:
					await message.reply_media_group(media)
					media.clear()
					continue
				video = video["src"]
				if ".mp4" in video:
					media.append(InputMediaVideo(video,caption=f"{username}"))
				else:
					media.append(InputMediaPhoto(video,caption=f"{username}"))
					
			await message.reply_media_group(media)
			media.clear()
			
@bot.on_message(filters.regex("^(http|https)://pin.it") & filters.private)
async def pint(bot,message):
	print("pint")
	#site = "home"
	msg = await message.reply("__جاري التحميل__")
	try:
		url = media(message.text)
		
		link = re.findall('<a id="downloadBtn" href="(.*?)" hidden rel="nofollow">',url)[0].replace("https://dl.cdn.io.vn/?url=","")
		#print(link)
		photo = re.findall('<div class="video-header mb-3"><img src="(.*?)" class="avatar"',url)[0]
			
		response= requests.get(photo)
		with open(f"{message.chat.id}.png", "wb") as file:
			file.write(response.content)
		#thumb = f"{message.chat.id}.png" 
		
		if download_video(link,f"video{message.chat.id}.mp4",message.chat.id):
			await bot.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_VIDEO) 
			await message.reply_video(
				open(f"video{message.chat.id}.mp4","rb"),
				caption=f'{username}',
				thumb=open(f"{message.chat.id}.png","rb")
				)
			os.remove(f"video{message.chat.id}.mp4")
			os.remove(f"{message.chat.id}.png")
			await msg.delete()
	except Exception as error:
		print(error)
		await msg.edit("**حدث خطأ**")
		await bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")
mis = {}
@bot.on_message(filters.regex("^(http|https)://(vm.|)tiktok.com") & filters.private)
async def tiktok(bot,message):
	print("tik")
	text = message.text
	msg = await message.reply("**جاري التحميل ...**")
	try:
		url = requests.get(f'https://tikwm.com/api/?url={text}').json()
		music = url['data']['music']
		region = url['data']['region']
		tit = url['data']['title']
		if "images" in str(url["data"].keys()):
			vid = url["data"]["images"]
		else:
			vid = url['data']['play']
		ava = url['data']['author']['avatar']
		rand = str("".join(random.choice("qwertyuiopasdfghjklzxcvbnm")for i in range(5)))+"getaudio"
		mis[rand] = music
		name = url['data']['music_info']['author']
		time = url['data']['duration']
		sh = url['data']['share_count']
		com = url['data']['comment_count']
		wat = url['data']['play_count']
		await msg.delete()
		await message.reply_photo(ava,caption=f'- اسم الحساب : **{name}**\n - دوله الحساب : **{region}**\n\n- عدد مرات المشاهدة : **{wat}**\n- عدد التعليقات : **{com}**\n- عدد مرات المشاركة : **{sh}**\n- طول الفيديو : **{time}**')
		if "list" in str(type(vid)):
			photos = []
			btns = km(
				[
					[
						btn('تحميل الصوت',callback_data=rand)
					]
				])
			for photo in vid:
				photos.append(InputMediaPhoto(photo,caption=f"{tit}"))
				if len(photos) ==10:
					await bot.send_media_group(
						message.chat.id,
						media=photos
					)
					photos.clear()
					continue
			await bot.send_media_group(message.chat.id,media=photos)
			await message.reply("هل تريد تحميل الصوت؟",reply_markup=btns)
			return
		btns = km(
				[
					[
						btn('تحميل الصوت',callback_data=rand)
					]
				]
			)
		await message.reply_video(
			vid,
			caption=f"{tit}",
			reply_markup=btns
		)
	except Exception as error:
		await message.reply('error );')
		await bot.send_message(dev,f"""Error:

الرابط: {text}

رسالة الخطأ: {str(error)}
""")
		
@bot.on_message(filters.regex("^(http|https)://(watch?v=|youtu.be/|shorts/youtu.be/|www.youtube.com/|youtube.com/)") & filters.private)
async def ytube(bot,message):
	print("youtube")
	try:
		vid_id = message.text.split("watch?v=")[1]
	except:
		try:
			vid_id = message.text.split("youtu.be/")[1].split("?")[0]
		except:
			try:
				vid_id = message.text.split("shorts/")[1].split("?")[0]
			except:
				vid_id = message.text.split("youtu.be/")[1]
	try:
		print(vid_id)
		yt = YoutubeSearch(f'https://youtu.be/{vid_id}', max_results=1).to_dict()
		title = yt[0]['title']
		print(title)
		url = f'https://youtu.be/{vid_id}'
		reply_markup = km(
			[
			
				[
					btn("صوت 💿", callback_data=f'{id}AUDIO{vid_id}'),
					btn("فيديو 🎥", callback_data=f'{id}VIDEO{vid_id}'),
				]
			
			])
		await message.reply_photo(
			str(yt[0]["thumbnails"][0].split("?")[0]),
			caption=f"**⤶ العنوان - [{title}]({url})**",
			reply_markup=reply_markup,
			#parse_mode="markdown"
		)
	except Exception as error:
		await message.reply('error );')
		await bot.send_message(dev,f"""Error:

الرابط: {vid_id}

رسالة الخطأ: {str(error)}
""")

@bot.on_message(filters.regex("^(@|)[a-zA-Z]") & filters.private)
async def instagram_s(bot,message):
	print("instagram_story")
	chat_id = message.chat.id
	if not "@" in message.text:
		user = message.text
	else:
		user = message.text.split("@")[1]
	#print()
	link = "https://instagram.com/"+user
	if what["adaa"] == "True" and message.from_user.id == dev:
		done = 0
		users = open("members.txt","r").readlines()
		for user in users:
			print(user)
			try:
				await message.copy(user,chat_id)
				done += 1
			except Exception as error:
				print(error)
				continue
		await message.reply(f"تم ارسال الاذاعة الى {done} من الاعضاء")
		what["adaa"] = "False"
		return
	headers = {
		'authority': 'reelsaver.net',
		'accept': '*/*',
		'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'origin': 'https://reelsaver.net',
		'referer': 'https://reelsaver.net/download-story-instagram',
		'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': generate_user_agent(),
		'x-requested-with': 'XMLHttpRequest'
	}
	data = {
		'via': 'form',
		'ref': 'download-story-instagram',
		'url': link,
	}
	response = requests.post('https://reelsaver.net/api/instagram',headers=headers,data=data).json()
	No = response['success']
	#print(response)
	if No == False:
		await message.reply('<i>خطأ تأكد من الرابط ..</i>')
	else:
		await bot.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)
		media = []
		#user = response['data']['user']['username']
		try:
			for video in response["data"]['medias']:
				if len(media) >= 10:
						await message.reply_media_group(media)
						media.clear()
						continue
				video = video["src"]
				print(media)
				if ".mp4" in video:
					media.append(InputMediaVideo(video,caption=f"{username}"))
				else:
					media.append(InputMediaPhoto(video,caption=f"{username}"))
						
			await message.reply_media_group(media)
			media.clear()
			
		except Exception as error:
			if "The media you tried to send is invalid" in str(error):
				for media in response["data"]['medias']:
					media = media["src"]
					if ".mp4" in media:
						await bot.send_video(message.chat.id,media)
					else:
						await bot.send_photo(message.chat.id,media)
				await message.reply("عذرًا Sir. تم ارسالها بشكل متقطع لان الحساب يحتوي على صورة متحركة في الاستوري خاصته، وانت تدري بعمو تلكرام مايخليك تدز صورة متحركة بمجموعة صور كـAlbum واحد")
						
@bot.on_message(filters.all & filters.private)
async def adaa(bot,message):
	chat_id = message.chat.id
	if what["adaa"] == "True" and message.from_user.id == dev:
		done = 0
		users = open("members.txt","r").readlines()
		for user in users:
			try:
				await message.copy(user,chat_id)
				done += 1
			except Exception as error:
				print(error)
				continue
		await message.reply(f"تم ارسال الاذاعة الى {done} من الاعضاء")
		what["adaa"] = "False"
		return
	#else:
#		await message.reply("`ارسل رابط فقط.`")
		
@bot.on_callback_query(filters.regex("AUDIO"))
def get_audio_from_youtube(bot, query):
	#id = query.data.split("AUDIO")[0]
	vid_id = query.data.split("AUDIO")[1]
	
	downloading = km([[btn("أنا بغدادي🌿",url="https://t.me/iBaghdady")]])
	uploading = km([[btn("أنا بغدادي🌿",url="https://t.me/iBaghdady")]])
	error = km([[btn("Error ⚠️",url="https://t.me/iBaghdady")]])
		
	query.edit_message_text("**جاري التحميل ..**", reply_markup=downloading)
	
	url = f'https://youtu.be/{vid_id}'
	ydl_ops = {"format": "bestaudio[ext=m4a]"}
	print(vid_id)
				
	with yt_dlp.YoutubeDL(ydl_ops) as ydl:
		info_dict = ydl.extract_info(url, download=False)
		if int(info_dict['duration']) > 5006:
			return query.edit_message_text("**⚠️ حد التحميل ساعة ونص فقط**",reply_markup=error)
			
		try:
			audio_file = ydl.prepare_filename(info_dict)
			ydl.process_info(info_dict)
			query.edit_message_text("**جاري الإرسال ..**", reply_markup=uploading)
			response= requests.get(info_dict['thumbnail'])
			with open(f"{vid_id}.png", "wb") as file:
				file.write(response.content)
			thumb = f"{vid_id}.png"
			msg = query.message.reply_audio(
				audio_file,
				title=info_dict['title'],
				duration=int(info_dict['duration']),
				performer=info_dict['channel'],
				#caption=f'• البحث من -› {user.mention}',
				thumb=thumb,
				reply_markup=downloading
			)
				
			query.edit_message_text("**تم التحميل.**",reply_markup=downloading)
				
			os.remove(audio_file)
			os.remove(thumb)
			return
		except Exception as err:
			print(str(err))
			query.edit_message_text("**⚠️ صار خطأ.**",reply_markup=error)
			bot.send_message(dev,f"""Error:

الرابط: {url}

رسالة الخطأ: {str(err)}
""")
			return
			
@bot.on_callback_query(filters.regex("VIDEO"))
def get_video_from_youtube(bot, query):
	#id = query.data.split("VIDEO")[0]
	vid_id = query.data.split("VIDEO")[1]
	
	downloading = km([[btn("أنا بغدادي🌿",url="https://t.me/iBaghdady")]])
	uploading = km([[btn("أنا بغدادي🌿",url="https://t.me/iBaghdady")]])
	error = km([[btn("Error ⚠️",url="https://t.me/iBaghdady")]])
	
	url = f'https://youtu.be/{vid_id}'
	query.edit_message_text("**جاري التحميل ..**", reply_markup=downloading)
	ydl_opts = {
		"format": "best",
		"keepvideo": True,
		"prefer_ffmpeg": False,
		"geo_bypass": True,
		"outtmpl": "%(title)s.%(ext)s",
		"quite": True,
	}
			
	with YoutubeDL(ydl_opts) as ytdl:
		ytdl_data = ytdl.extract_info(url, download=True)
		#print(ytdl_data["title"])
		if int(ytdl_data['duration']) > 5006:
			return query.edit_message_text("**⚠️ حد التحميل ساعة ونص فقط**",reply_markup=error)
		
		try:
			file_name = ytdl.prepare_filename(ytdl_data)
			query.edit_message_text("**جاري الإرسال ..**", reply_markup=uploading)
			response= requests.get(ytdl_data['thumbnail'])
			with open(f"{vid_id}.png", "wb") as file:
				file.write(response.content)
			thumb = f"{vid_id}.png"
			#user = bot.get_users(int(id))	
			msg = query.message.reply_video(
				file_name,
				duration=int(ytdl_data['duration']),
				#caption=f'• البحث من  -› {user.mention}',
				thumb=thumb,
				reply_markup=downloading
			)
			os.remove(file_name)
			os.remove(thumb)
			query.edit_message_text("**تم التحميل.**")
		except Exception as err:
			print(str(err))
			query.edit_message_text("**⚠️ صار خطأ.**",reply_markup=error)
			bot.send_message(dev,f"""Error:

الرابط: {url}

رسالة الخطأ: {str(err)}
""")
			return
@bot.on_callback_query(filters.regex("getaudio"))
def get_audio_tiktok(bot, query):
	if mis[query.data]:
		audio = mis[query.data].split("getaudio")[0]
		print(audio)
		query.message.delete()
		return query.message.reply_audio(audio)
@bot.on_callback_query(filters.regex("^(stats|adaa|back)$"))
def setin(bot, query):
	back = km([
		[btn(text = "رجوع",callback_data="back")]
		]
		)
	if query.data == "stats":
		users = 0
		for i in open("members.txt","r").readlines():
			if i != "\n":
				users += 1
		query.message.edit(f"""
قائمة الاعضاء.

عدد الاعضاء: {users}""",
			reply_markup=back
		)
	elif query.data == "adaa":
		query.message.edit("تمام، دز اارسالة وراح ادزها للكل تدلل سيدي.",reply_markup=back)
		what["adaa"] = "True"
		
	elif query.data == "back":
		query.message.edit("مرحبا بك سيدي في بوتك اختر ادناه...",reply_markup=btns)
		what["adaa"] = "False"
print("شغال")
#keep_alive()
idle()