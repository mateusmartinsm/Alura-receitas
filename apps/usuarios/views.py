from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
	""" Cadastra uma nova pessoa no sistema """
	# verificando o recebimento dos dados
	if request.method == 'POST':
		nome = request.POST['nome']
		email = request.POST['email']
		senha = request.POST['password']
		senha2 = request.POST['password2']
		if campo_vazio(nome):
			messages.error(request, f'O campo nome não pode ficar em branco')
			return redirect('cadastro')
		if campo_vazio(email):
			messages.error(request, f'O campo email não pode ficar em braco')
			return redirect('cadastro')
		if senhas_diferentes(senha, senha2):
			messages.error(request, 'As senhas não são iguais')
			return redirect('cadastro')
		if User.objects.filter(email=email).exists():
			messages.error(request, 'Usuario já cadastrado')
			return redirect('cadastro')
		if User.objects.filter(username=nome).exists():
			messages.error(request, 'Usuario já cadastrado')
			return redirect('cadastro')
		user = User.objects.create_user(username=nome, email=email, password=senha)
		user.save()
		messages.success(request, 'cadastro realizado com sucesso')
		return redirect('login')
	return render(request, 'usuarios/cadastro.html')

def login(request):
	""" Realiza o login de uma pessoa no sistema """
	if request.method == 'POST':
		email = request.POST['email']
		senha = request.POST['senha']
		if campo_vazio(email) or campo_vazio(senha):
			messages.error(request, 'Os campos email e senha não podem ficar em branco')
			return redirect('login')
		if User.objects.filter(email=email).exists():
			nome = User.objects.filter(email=email).values_list('username', flat=True).get()
			user = auth.authenticate(request, username=nome, password=senha)
			if user is not None:
				auth.login(request, user)
				messages.success(request, 'Login realizado com sucesso')				
				return redirect('dashboard')
		messages.error(request, 'Usuario ou senha incorreta')
	return render(request, 'usuarios/login.html')

def logout(request):
	auth.logout(request)
	return redirect('index')

def dashboard(request):
	if request.user.is_authenticated:
		id = request.user.id
		receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)
		dados = {'receitas':receitas}
		return render(request, 'usuarios/dashboard.html', dados)
	return redirect('index')

def campo_vazio(campo):
	return not campo.strip()

def senhas_diferentes(senha, senha2):
	return senha != senha2