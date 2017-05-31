# #encoding: utf-8
import wx
import os
import os.path
import json
import subprocess

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1, u"DuDu车专", size = (500, 600))
		panel = wx.Panel(self, -1)

		self.staticFileList=wx.StaticText(panel, -1, u"文件/文件夹：")
		self.fileCount=wx.StaticText(panel,-1,u"n个")
		self.fileText = wx.TextCtrl(panel, -1, "")

		self.staticVideo=wx.StaticText(panel,-1,u"视频：")
		self.videoEnabled=wx.CheckBox(panel,-1,u"启用")
		self.videoInfo=wx.StaticText(panel,-1,u"Video Info:")

		self.staticVideoEncoder=wx.StaticText(panel,-1,u"输出编码：")
		self.videoEncoderList=[u'copy',u'h264',u'libx265',u'自动']
		self.videoEncoder=wx.Choice(panel,-1,choices=self.videoEncoderList)
		self.staticVideoExtra=wx.StaticText(panel,-1,u"额外参数：")
		self.videoExtra=wx.TextCtrl(panel,-1,"")

		self.staticAudio=wx.StaticText(panel,-1,u"音频：")
		self.audioEnabled=wx.CheckBox(panel,-1,u"启用")
		self.audioInfo=wx.StaticText(panel,-1,u"Audio Info:")

		self.staticAudioEncoder=wx.StaticText(panel,-1,u"输出编码：")
		self.audioEncoderList=[u'copy',u'aac',u'pcm_s16le',u'自动']
		self.audioEncoder=wx.Choice(panel,-1,choices=self.audioEncoderList)
		self.staticAudioExtra=wx.StaticText(panel,-1,u"额外参数：")
		self.audioExtra=wx.TextCtrl(panel,-1,"")

		self.staticContainer=wx.StaticText(panel,-1,u"封装格式：")
		self.containerList=[u'MP4',u'MOV',u'AAC',u'WAV']
		self.container=wx.Choice(panel,-1,choices=self.containerList)

		self.overWrite=wx.CheckBox(panel,-1,u'覆盖重名文件')

		self.staticCMD=wx.StaticText(panel,-1,u"命令行：")
		# self.cmdText=wx.TextCtrl(panel,-1,"ffmpeg -i")
		self.cmdText=wx.TextCtrl(panel,-1,"ffmpeg -i",style=wx.TE_MULTILINE)

		self.btn=wx.Button(panel,label="Go!")


		# file related
		filehBox=wx.BoxSizer()
		filehBox.Add(self.staticFileList,0,wx.LEFT|wx.ALIGN_CENTER,5)
		filehBox.Add(self.fileCount,1,wx.LEFT|wx.ALIGN_CENTER,10)

		filevBox=wx.BoxSizer(wx.VERTICAL)
		filevBox.Add(filehBox,0,wx.ALL,10)
		filevBox.Add(self.fileText,1,wx.EXPAND|wx.LEFT|wx.RIGHT,15)


		# video related
		vhBoxEnable=wx.BoxSizer()
		vhBoxEnable.Add(self.staticVideo,0,wx.LEFT|wx.ALIGN_CENTER,10)
		vhBoxEnable.Add(self.videoEnabled,0,wx.LEFT|wx.ALIGN_CENTER,10)
		vhBoxEnable.Add(self.videoInfo,0,wx.LEFT|wx.ALIGN_CENTER,10)

		vhBoxEncoder=wx.BoxSizer()
		vhBoxEncoder.Add(self.staticVideoEncoder,0,wx.LEFT|wx.ALIGN_CENTER,10)
		vhBoxEncoder.Add(self.videoEncoder,0,wx.LEFT|wx.ALIGN_CENTER,10)

		vhBoxExtra=wx.BoxSizer()
		vhBoxExtra.Add(self.staticVideoExtra,0,wx.LEFT|wx.ALIGN_CENTER,10)
		vhBoxExtra.Add(self.videoExtra,1,wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,10)

		vvBox=wx.BoxSizer(wx.VERTICAL)
		vvBox.Add(vhBoxEnable,0,wx.EXPAND|wx.ALL,10)
		vvBox.Add(vhBoxEncoder,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,10)
		vvBox.Add(vhBoxExtra,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,10)

		# audio related
		ahBoxEnable=wx.BoxSizer()
		ahBoxEnable.Add(self.staticAudio,0,wx.LEFT|wx.ALIGN_CENTER,10)
		ahBoxEnable.Add(self.audioEnabled,0,wx.LEFT|wx.ALIGN_CENTER,10)
		ahBoxEnable.Add(self.audioInfo,0,wx.LEFT|wx.ALIGN_CENTER,10)

		ahBoxEncoder=wx.BoxSizer()
		ahBoxEncoder.Add(self.staticAudioEncoder,0,wx.LEFT|wx.ALIGN_CENTER,10)
		ahBoxEncoder.Add(self.audioEncoder,0,wx.LEFT|wx.ALIGN_CENTER,10)

		ahBoxExtra=wx.BoxSizer()
		ahBoxExtra.Add(self.staticAudioExtra,0,wx.LEFT|wx.ALIGN_CENTER,10)
		ahBoxExtra.Add(self.audioExtra,1,wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,10)

		avBox=wx.BoxSizer(wx.VERTICAL)
		avBox.Add(ahBoxEnable,0,wx.EXPAND|wx.ALL,border=10)
		avBox.Add(ahBoxEncoder,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,border=10)
		avBox.Add(ahBoxExtra,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER,border=10)

		chBox=wx.BoxSizer()
		chBox.Add(self.staticContainer,0,wx.LEFT|wx.ALIGN_CENTER,20)
		chBox.Add(self.container,0,wx.ALL|wx.ALIGN_CENTER,5)
		chBox.Add(self.overWrite,0,wx.LEFT|wx.ALIGN_CENTER,30)

		# global
		globalBox=wx.BoxSizer(wx.VERTICAL)
		globalBox.Add(filevBox,0,wx.EXPAND|wx.ALL,10)
		globalBox.Add(vvBox,0,wx.EXPAND|wx.ALL,5)
		globalBox.Add(avBox,0,wx.EXPAND|wx.ALL,5)
		globalBox.Add(chBox,0,wx.EXPAND|wx.ALL,5)
		globalBox.Add(self.staticCMD,0,wx.EXPAND|wx.ALL,10)
		globalBox.Add(self.cmdText,1,wx.EXPAND|wx.ALL,10)
		globalBox.Add(self.btn,0,wx.EXPAND|wx.ALL,10)

		panel.SetSizer(globalBox)
		panel.Layout()




	# def OnMove(self, event):
	# 	pass
	# 	# pos = event.GetPosition()
	# 	# self.posCtrl.SetValue("%s, %s" %(pos.x, pos.y))


def updateInfo(filePath):

	cmd='ffprobe -v quiet -print_format json -show_format -show_streams "%s" > mediaInfo.json' % filePath
	# print(cmd)
	# ffprobe=subprocess.Popen(['ffprobe',cmd.encode('utf-8')])
	# ffprobe.wait()
	os.system(cmd.encode('gbk'))
	mediaInfo=json.loads(open('mediaInfo.json').read())

	frame.videoInfo.SetLabel("")
	frame.audioInfo.SetLabel("")

	for s in mediaInfo['streams']:
		if s['codec_type'] == 'video':
			videoInfoStr=s['codec_name']
			if 'pix_fmt' in s and s['pix_fmt']=='bgra':
				videoInfoStr+='(alpha)'

			videoInfoStr+=', '+str(s['width'])+'*'+str(s['height'])+', '+s['display_aspect_ratio']
			
			if 'avg_frame_rate' in s:
				fr=s['avg_frame_rate']
				(a,b)=fr.split('/')
				if int(b)==0:
					b=1

				fps=float(a)/float(b)
				if int(fps)==fps:
					fps=int(fps)
				else:
					fps=round(fps,3)
				videoInfoStr+=', '+str(fps)+'fps'

			if 'bit_rate' in s:
				br=s['bit_rate']
				br=float(br)/1000
				if(br>1000):
					br=str(round(br/1000,2))+'Mb/s'
				else:
					br=str(round(br,2))+'Kb/s'
				videoInfoStr+=', '+br

			if 'duration' in s:
				sDuration=float(s['duration'])
				second=int(sDuration)
				miliSecond=sDuration-second
				hour=minute=0
				if(second>60):
					minute=int(second/60)
					second=second-minute*60
					if minute>60:
						hour=int(minute/60)
						minute=minute-hour*60

				videoInfoStr+=' ,'
				if hour>0:
					if hour<10 :	videoInfoStr+='0'
					videoInfoStr+=str(hour)+':'
				else:
					videoInfoStr+='00:'
				if minute>0:
					if minute<10 :	videoInfoStr+='0'
					videoInfoStr+=str(minute)+':'
				else:
					videoInfoStr+='00:'
				if second>0:
					if second<10 :	videoInfoStr+='0'
					videoInfoStr+=str(second)+'.'
				else:
					videoInfoStr+='00.'
				videoInfoStr+=str(round(miliSecond,3))[2:]	


			frame.videoInfo.SetLabel(videoInfoStr)

		elif s['codec_type'] == 'audio':
			audioInfoStr=s['codec_name']+', '+str(float(s['sample_rate'])/1000)+'kHz'

			if 'channel_layout' in s:
				audioInfoStr+=', '+s['channel_layout']
			else:
				if 'channels' in s and s['channels']==1:
					audioInfoStr+=', '+'mono'

			if 'bit_rate' in s:
				audioInfoStr+=', '+str(float(s['bit_rate'])/1000)+'kb/s'

			frame.audioInfo.SetLabel(audioInfoStr)


def getFileList(fileStr):

	fileList=[]

	fileStr=frame.fileText.GetValue()

	stype="N/A"
	if not os.path.exists(fileStr):
		nfileCount=0
	else:
		if os.path.isfile(fileStr):
			nfileCount=1
			fileList=[fileStr]
			stype='file'
			updateInfo(fileStr)
		else:
			fileList=[os.path.join(fileStr,file) for file in os.listdir(fileStr) if os.path.isfile(os.path.join(fileStr,file))]
			nfileCount=len(fileList)
			stype='folder'
			updateInfo(fileList[0])
	
	frame.fileCount.SetLabel(str(nfileCount)+u'个')
	return (nfileCount,stype)

def findNextUsable(boverWrite,part1,part2):
	if boverWrite or (not os.path.exists(part1+part2)):
		return part1+part2
	else:
		iter=1
		while  True:
			testPath=part1+'-'+str(iter)+part2
			if not os.path.exists(testPath):
				return testPath
			iter+=1

def updateCmd(event):

	inputPathStr=frame.fileText.GetValue()
	newInputPathStr=inputPathStr.replace('"','')
	if newInputPathStr != inputPathStr:
		frame.fileText.SetValue(newInputPathStr)
	# frame.fileText.SetValue(inputPathStr)

	(nfileCount,stype)=getFileList(inputPathStr)	

	cmd='%sffmpeg -i "%s"'

	# overwrite
	boverWrite= False
	if frame.overWrite.GetValue() == wx.CHK_CHECKED:
		cmd+=' -y'
		boverWrite=True

	# video enabled
	if frame.videoEnabled.GetValue() == wx.CHK_CHECKED:
		vcodecStr=frame.videoEncoder.GetStringSelection()
		if vcodecStr != u'自动':
			cmd+=' -vcodec '+vcodecStr
		extra=frame.videoExtra.GetValue()
		if extra != "":
			cmd+=' '+ extra
	else:
		cmd+=' -vn'

	# audio enabled
	if frame.audioEnabled.GetValue() == wx.CHK_CHECKED:
		acodecStr=frame.audioEncoder.GetStringSelection()
		if acodecStr != u'自动':
			cmd+=' -acodec '+acodecStr
		extra=frame.audioExtra.GetValue()
		if extra != "":
			cmd+=' '+ extra
	else:
		cmd+=' -an'

	#container
	outputExt=frame.container.GetStringSelection()

	cmd+=' "%s"'

	if stype == 'N/A':
		frame.fileCount.SetLabel(u'无效路径')
		return

	if stype == 'file':		
		(inputPath,inputExt)=os.path.splitext(inputPathStr)
		outFileName=findNextUsable(boverWrite,inputPath+'-converted','.'+outputExt)
		cmd= cmd % ('',inputPathStr,outFileName)
	else:
		inputFiles='"'+os.path.join(inputPathStr,'*.*')+'"'	
		outDir=os.path.join(inputPathStr,'converted')
		outDir=findNextUsable(boverWrite,outDir,'')
		# if not os.path.exists(outDir):
		# 	os.mkdir(outDir)

		outFileName=os.path.join(outDir,'%~ni.'+outputExt)
		cmd= cmd % ('for %i in ('+inputFiles+') do ','%i',outFileName)
		cmd='mkdir "%s" & ' % outDir+cmd

	frame.cmdText.SetValue(cmd)
	# print('updated cmd: '+ cmd)

def RunCmd(event): 

	# print('running cmd: '+frame.cmdText.GetValue())
	cmd=frame.cmdText.GetValue()
	os.system(cmd.encode('gbk'))
	# os.system('cmd /c '+cmd.encode('gbk'))


class MyFileDropTarget(wx.FileDropTarget):
	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window
	def OnDropFiles(self, x, y, filenames):
		self.window.fileText.SetValue(filenames[0])

		# for file in filenames:
		# 	self.window.AppendText("\t%s\n" % file)



if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame()
	frame.Show(True)
	frame.videoEnabled.SetValue(wx.CHK_CHECKED)
	frame.audioEnabled.SetValue(wx.CHK_CHECKED)
	frame.videoEncoder.SetSelection(0)
	frame.audioEncoder.SetSelection(0)
	frame.container.SetSelection(0)

	frame.btn.Bind(wx.EVT_BUTTON,RunCmd)
	frame.fileText.Bind(wx.EVT_TEXT,updateCmd)
	frame.fileText.SetValue(u"D:\电影\老炮儿 Mr.Six.2015.1080p.WEB-DL.x264.AC3-SeeHD.mkv")
	
	frame.videoEnabled.Bind(wx.EVT_CHECKBOX,updateCmd)
	frame.audioEnabled.Bind(wx.EVT_CHECKBOX,updateCmd)
	frame.overWrite.Bind(wx.EVT_CHECKBOX,updateCmd)

	frame.videoEncoder.Bind(wx.EVT_CHOICE,updateCmd)
	frame.audioEncoder.Bind(wx.EVT_CHOICE,updateCmd)
	frame.container.Bind(wx.EVT_CHOICE,updateCmd)

	frame.videoExtra.Bind(wx.EVT_TEXT,updateCmd)
	frame.audioExtra.Bind(wx.EVT_TEXT,updateCmd)


	dt = MyFileDropTarget(frame)
	frame.SetDropTarget(dt)

	app.MainLoop()
