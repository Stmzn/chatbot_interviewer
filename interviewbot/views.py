from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SimpleForm
from django.urls import reverse_lazy
from .models import Interview,PersonalDetails
from django.shortcuts import redirect
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
from django.contrib.auth.decorators import login_required

@login_required
def load_homepage(request):
	if request.user.is_superuser:
		return redirect('interview:temp')
	else:
		try:
			personaldetails = PersonalDetails.objects.get(user = request.user.id)
			print(personaldetails.status)
			if(personaldetails.status == 'Accepted'):
				return render(request, 'interviewbot/home.html',{'notification':'Congragulations !!! You are Accepted. We will contact you via Mail'})
			elif(personaldetails.status == 'Rejected'):
				return render(request, 'interviewbot/home.html',{'notification':'Sorry, You are Rejected'})
			else:
				return render(request, 'interviewbot/home.html')
		except:
			return render(request,'interviewbot/home.html')


@login_required
class PersonalDetailsView(CreateView):
	template_name = 'interviewbot/chat.html'
	form_class = SimpleForm
	success_url = reverse_lazy('')

	def form_valid(self,form):
		if form.is_valid():
			pass

	def form_invalid(self,form):
		print('invalid form')


@login_required
def personalform(request):
	if request.POST:
		if not request.POST['firstname']:
			return render(request, 'interviewbot/basic_details2.html',{'error':'Please Enter First Name',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber'),'option_select':request.POST.get('option_select')})
		if not request.POST['email']:
			return render(request, 'interviewbot/basic_details2.html',{'error':'Please Enter Email',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber'),'option_select':request.POST.get('option_select')})
		if not request.POST['interviewnumber']:
			return render(request, 'interviewbot/basic_details2.html',{'error':'Please Enter Interview Number',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber'),'option_select':request.POST.get('option_select')})
		try:
			request.FILES['file']

		except:
			return render(request, 'interviewbot/basic_details2.html', {'error': 'Please Insert File',
																		'firstname': request.POST.get('firstname'),
																		'email': request.POST.get('email'),
																		'interviewnumber': request.POST.get(
																			'interviewnumber'),
																		'option_select': request.POST.get(
																			'option_select')})
		pdf_file = request.FILES['file']


		if not pdf_file.name:
			return render(request, 'interviewbot/basic_details2.html',{'error':'Please Upload File',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber')})

		if (pdf_file.name.split('.')[-1] != 'pdf') and (pdf_file.name.split('.')[-1] != '.docx'):
			return render(request, 'interviewbot/basic_details2.html',{'error':'Invlid File Format',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber')})

		if (request.POST['interviewnumber']  not in ['3345','2904','1996']):
			return render(request, 'interviewbot/basic_details2.html',{'error':'Please Enter Valid Interview Number',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber')})


		pdf_text = pdf_file.read()
		rsrcmgr = PDFResourceManager()
		retstr = io.StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		pdf_text = io.BytesIO(pdf_text)
		fp = pdf_text
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos = set()

		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
		                              password=password,
		                              caching=caching,
		                              check_extractable=True):
		    interpreter.process_page(page)

		text = retstr.getvalue()
		device.close()
		retstr.close()

		initial_status = 'Accepted'
		if request.POST['option_select'] == 'Python Developer':
			if not 'python' in text:
				initial_status = 'Rejected'
		if request.POST['option_select'] == 'Java Developer':
			if not 'java' in text:
				initial_status = 'Rejected'


		current_user = request.user

		
		try:
			# user = personaldetails.user
			personaldetails = PersonalDetails.objects.get(user = current_user.id)
			return render(request, 'interviewbot/basic_details2.html',{'error':'You Have Already Given Interview',
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber')})
		except:
			personaldetails = PersonalDetails()
			personaldetails.user = current_user.id
			personaldetails.first_name = request.POST['firstname']
			personaldetails.email_id = request.POST['email']
			personaldetails.interview_number = request.POST['interviewnumber']
			personaldetails.interview_type = request.POST['option_select']
			personaldetails.cv_file = request.FILES['file']
			personaldetails.initial_status = initial_status
			personaldetails.status = 'Not Decided'
			personaldetails.save()

			unique_id = personaldetails.id

			request.session['details_filled'] = True
			request.session['previous_question'] = 0
			request.session['unique_id'] = unique_id

		return redirect('interview:home')
	else:
		return render(request, 'interviewbot/basic_details2.html')


@login_required
def about(request):
	return render(request,'interviewbot/about.html')

@login_required
def personaldetails(request):
	if request.POST:
		pass

@login_required
def main_template(request):
	return render(request, 'interviewbot/chat.html')

@login_required
def initial_load(request):
	print('how is it going')
	question = "Can you please introduce your self (your name, nationality, age)?"
	request.session['previous_question'] = 0
	request.session['python_included'] = False
	request.session['js_included'] = False
	request.session['no_output'] = False
	request.session['score'] = 0
	try:
		request.session['details_filled']
		del request.session['details_filled']
		# del request.session['unique_id']ss
		return render(request, 'interviewbot/initial_chat.html', {'question':question,'success':"True"})
	except:
		return render(request, 'interviewbot/initial_chat.html', {'success':"False"})		

@login_required
def load_reply(request):
	questions = ["Do you have any experience of coding?",
	"Could you please list your preferred coding languages?",
	"Do you know about the Data analytics?",
	"Can you please elaborate?",
	"Since you know some Javascript, have you work in any mobile application frameworks, if yes please let me know what is it",
	"Have you ever worked in any project in Computer science industry?",
	"Can please talk about it?",
	"How many years of experience do you have?",
	"This job requires strict time management. Would you be able to handle the sudden meetings that may occur",
	"Talk a little bit about your self."]
	
	flag = 0
	try:
		request.session['previous_question']
		interview = Interview()
		interview.interview_number = request.session['unique_id']
		interview.questions = questions[request.session['previous_question']]
		interview.answers = request.GET.get('text')
		interview.save()
	except:
		request.session['previous_question'] = 0
		flag = 1
	if(request.session['no_output']):
		return render(request, 'interviewbot/chat_display.html', {'success':"False"})

	if(flag == 0):
		if(request.session['previous_question'] == len(questions)):
			request.session['previous_question'] = 0
	else:
		request.session['previous_question'] = 0

	text = request.GET.get('text')


	if(request.session['python_included'] == False and request.session['js_included'] == False):
		if(request.session['previous_question'] == 1):
			if('python' in text.lower().split(' ')):
				request.session['python_included'] = True
			elif('python' in text.lower().split(',')):
				request.session['python_included'] = True
			if('javascript' in text.lower().split(' ')):
				request.session['js_included'] = True
			elif('javascript' in text.lower().split(',')):
				request.session['js_included'] = True

	if(request.session['previous_question'] == 0):
		if 'yes' in text.lower().split(' '):
			request.session['score'] += 1
	if( (request.session['previous_question'] == 1) or (request.session['previous_question'] == 2) or (request.session['previous_question'] == 3) ):
		if request.session['python_included']:
			request.session['score'] += 1
			request.session['python_included'] = False
			request.session['previous_question'] = 2
			return render(request, 'interviewbot/chat_display.html', {'text': text,'question':questions[request.session['previous_question']],'success':"True","continue":True})

		elif "yes" in text.strip().lower():
			request.session['score'] += 1
			request.session['previous_question'] = 3
			return render(request, 'interviewbot/chat_display.html', {'text': text,'question':questions[request.session['previous_question']],'success':"True","continue":True})

		elif request.session['js_included']:
			request.session['score'] += 1
			request.session['js_included'] = False
			request.session['previous_question'] = 4
			return render(request, 'interviewbot/chat_display.html', {'text': text,'question':questions[request.session['previous_question']],'success':"True","continue":True})
		else:
			request.session['previous_question'] = 5
			return render(request, 'interviewbot/chat_display.html', {'text': text,'question':questions[request.session['previous_question']],'success':"True","continue":True})

	elif(request.session['previous_question'] == 5):
		if('yes' in text.lower().split(' ')):
			request.session['score'] += 1
			request.session['previous_question'] += 1
		else:
			request.session['previous_question'] += 2

	elif(request.session['previous_question'] == len(questions)-1):
		del request.session['previous_question']
		return redirect('interview:home')
	else:
		request.session['previous_question'] += 1

	if(request.session['previous_question'] < len(questions) - 1):
		return render(request, 'interviewbot/chat_display.html', {'text': text,'question':questions[request.session['previous_question']],'success':"True","continue":True})
	else:
		if(request.session['no_output'] == False):
			request.session['no_output']  = True
			if(request.session['score'] > 3):
				interview = Interview()
				interview.interview_number = request.session['unique_id']
				interview.questions = 'score'
				interview.answers = "Qualified Candidate"
				interview.save()
			else:
				interview = Interview()
				interview.interview_number = request.session['unique_id']
				interview.questions = 'score'
				interview.answers = "Not Qualified Candidate"
				interview.save()

			return render(request, 'interviewbot/chat_display.html', {'text': text,'question':'Thanks for Giving Interview. We will contact you via Mail.','success':"True","continue":True})						


@login_required
def interviewer_page(request):
	personal_details = PersonalDetails.objects.all()
	output_array = []
	for i in personal_details:
		if(i.initial_status == 'Accepted'):
			output = {}
			output['hidden_id'] = i.id
			output['id'] = i.first_name
			output['interview_number'] = i.interview_number
			output['job'] = i.interview_type
			if(i.status == 'Accepted'):
				output['status'] = i.status
			elif(i.status == 'Rejected'):
				output['status'] = i.status
			output_array.append(output)
	return render(request, 'interviewbot/interviewer_display.html', {'output':output_array})

@login_required
def set_accept(request):
	status = 'Accepted'
	current_id = request.GET['value']
	personaldetails = PersonalDetails.objects.get(id = current_id)
	personaldetails.status = status
	personaldetails.save()
	return render(request, 'interviewbot/interviewer_display.html', {'output':''})

@login_required
def set_reject(request):
	status = 'Rejected'
	current_id = request.GET['value']
	print(current_id)
	personaldetails = PersonalDetails.objects.get(id = current_id)
	personaldetails.status = status
	personaldetails.save()
	print('saved')
	return render(request, 'interviewbot/interviewer_display.html', {'output':''})

@login_required
def application_result(request):
	try:
		print(request.user.id)
		print('weruoiwerujdsfusdgfu8976875667')
		personal_details = PersonalDetails.objects.get(user = request.user.id)
		output_array = []
		output = {}
		output['id'] = personal_details.first_name
		output['status'] = personal_details.initial_status
		if(personal_details.initial_status == 'Accepted'):
			output['status'] = personal_details.initial_status
		elif(personal_details.initial_status == 'Rejected'):
			output['status'] = personal_details.initial_status
		output_array.append(output)
		return render(request, 'interviewbot/interview.html', {'output':output_array})
	except:
		return render(request, 'interviewbot/interview.html')

@login_required
def redirect_interview(request):
	current_user = request.user
	try:
		personaldetails = PersonalDetails.objects.get(user = current_user.id)
		if personaldetails.initial_status == 'Accepted':
			return render(request, 'interviewbot/chat.html')
		else:
			return render(request, 'interviewbot/interview.html',{'error':"You are not Selected based on Resume"})
	except:
		return render(request, 'interviewbot/basic_details2.html',{'error':"Please fill basic details first",
				'firstname':request.POST.get('firstname'),'email':request.POST.get('email'),
				'interviewnumber':request.POST.get('interviewnumber')})
