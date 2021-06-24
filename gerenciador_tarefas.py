import pygame
import psutil
import cpuinfo
import os
import time

BRANCO = (255,255,255)
PRETO = (0,0,0)
LARANJA = (246,130,0)
VERMELHO = (230,0,0)
AZUL = (0,0,255)
CINZA = (200, 200, 200)

pygame.init()
largura_tela, altura_tela = 1024, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
tela.fill(BRANCO)
pygame.font.init()
        

def mostra_texto(texto, pos, cor, cent=False, bold=False):
    if bold:
        font = pygame.font.SysFont('calibri', 22, bold=True)
    else:
        font = pygame.font.SysFont('calibri', 22)
    text = font.render(f"{texto}", 1, cor)
    if cent:
        textpos = text.get_rect(center=pos,)
        tela.blit(text, textpos)
    else:
        tela.blit(text, pos)

def desenha_abas():
    aba0 = pygame.Rect(1, 0, 204, 50)
    pygame.draw.rect(tela, PRETO, aba0)
    mostra_texto("CPU",(102.5,25), BRANCO, cent=True, bold=True)

    aba1 = pygame.Rect(206, 0, 203, 50)
    pygame.draw.rect(tela, PRETO, aba1)
    mostra_texto("Memória",(307.5,25), BRANCO, cent=True, bold=True)

    aba2 = pygame.Rect(410, 0, 204, 50)
    pygame.draw.rect(tela, PRETO, aba2)
    mostra_texto("Rede",(511.5,25), BRANCO, cent=True, bold=True)

    aba3 = pygame.Rect(615, 0, 204, 50)
    pygame.draw.rect(tela, PRETO, aba3)
    mostra_texto("Arquivos",(716.5,25), BRANCO, cent=True, bold=True)

    aba4 = pygame.Rect(820, 0, 203, 50)
    pygame.draw.rect(tela, PRETO, aba4)
    mostra_texto("Processos",(921.5,25), BRANCO, cent=True, bold=True)
    return [aba0, aba1, aba2, aba3, aba4]

def arquivos():
    lista = os.listdir()
    dic = {} 
    for i in lista:
        if os.path.isfile(i):
            dic[i] = []
            dic[i].append(os.stat(i).st_size) # Tamanho
            dic[i].append(os.stat(i).st_atime) # Tempo de criação

    texto = "Tamanho"
    mostra_texto(texto, (20, 120), PRETO, bold=True)
    texto = "Data de Criação"
    mostra_texto(texto, (220, 120), PRETO, bold=True)
    texto = "Nome"
    mostra_texto(texto, (520, 120), PRETO, bold=True)

    y=150
    for i in dic:
        kb = dic[i][0]/1000
        texto = f'{kb:.2f} KB'
        mostra_texto(texto, (20, y), PRETO)
        dia = time.ctime(dic[i][1])
        mostra_texto(dia, (220, y), PRETO)
        texto = i
        mostra_texto(i, (520, y), PRETO)
        y = y+30

def info_proc(pid, y):
    try:
        p = psutil.Process(pid)
        texto = f'{pid}'
        mostra_texto(texto, (20, y), PRETO)
        texto = f'{p.num_threads()}'
        mostra_texto(texto, (120, y), PRETO)
        texto = f'{p.cpu_times().user:.2f}'
        mostra_texto(texto, (290, y), PRETO)
        texto = f'{p.cpu_times().system:.2f}'
        mostra_texto(texto, (460, y), PRETO)
        texto = f'{p.memory_percent():.2f} MB'
        mostra_texto(texto, (630, y), PRETO)
        exe = p.exe().split('\\')
        texto = f"{exe[-1]}"
        mostra_texto(texto, (800,y), PRETO)
    except:
        pass 

def processos():
    texto = "PID"
    mostra_texto(texto, (20, 120), PRETO, bold=True)
    texto = "# Threads"
    mostra_texto(texto, (120, 120), PRETO, bold=True)
    texto = "T. Usu."
    mostra_texto(texto, (290, 120), PRETO, bold=True)
    texto = "T. Sis."
    mostra_texto(texto, (460, 120), PRETO, bold=True)
    texto = "Mem.(%)"
    mostra_texto(texto, (630, 120), PRETO, bold=True)
    texto = "Executável"
    mostra_texto(texto, (800, 120), PRETO, bold=True)
    lista = psutil.pids()
    lista = lista[:15]
    y = 150
    for i in lista:
        info_proc(i, y)
        y = y + 30

def memoria():
    disco = psutil.disk_usage('.')
    text = f"Total:"
    mostra_texto(text,(20,120), PRETO, bold=True)
    text = f"{format_memory(disco.total)} GB"
    mostra_texto(text,(120,120), PRETO)
    text = f"Em uso:"
    mostra_texto(text,(20,140), PRETO, bold=True)
    text = f"{format_memory(disco.used)} GB"
    mostra_texto(text,(120,140), PRETO)
    text = f"Livre:"
    mostra_texto(text,(20,160), PRETO, bold=True)
    text = f"{format_memory(disco.free)} GB"
    mostra_texto(text,(120,160), PRETO)
    text = f"Percentual de Disco Usado:"
    mostra_texto(text,(20,200), PRETO, bold=True)
    text = f"{disco.percent:}%"
    mostra_texto(text,(280,200), PRETO)

def mostra_uso_disco():
    disco = psutil.disk_usage('.')
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 260, larg, 50))
    larg = larg*disco.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 260, larg, 50))
    total = format_memory(disco.total)
    texto_barra = "Uso de Disco (Total: " + str(total) + " GB):"
    mostra_texto(texto_barra, (20,240), PRETO, bold=True)

def mostra_uso_memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, AZUL, (20, 370, larg, 50))
    larg = larg*mem.percent/100
    pygame.draw.rect(tela, VERMELHO, (20, 370, larg, 50))
    total = format_memory(mem.total)
    texto_barra = "Uso de Memória (Total: " + str(total) + " GB):"
    mostra_texto(texto_barra, (20,350), PRETO, bold=True)

def format_memory(info):
    return round(info/(1024*1024*1024), 2)

def texto_cpu(s1, nome, chave, pos_y):
    font = pygame.font.SysFont('calibri', 22, bold=True)
    text = font.render(nome, True, PRETO)
    s1.blit(text, (10, pos_y))
    info_cpu = cpuinfo.get_cpu_info()
    if chave == "freq":
        s = str(round(psutil.cpu_freq().current, 2))
    elif chave == "nucleos":
    	s = str(psutil.cpu_count())
    	s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    else:
        s = str(info_cpu[chave])
        
    font = pygame.font.SysFont('calibri', 22)
    text = font.render(s, True, PRETO)
    s1.blit(text, (200, pos_y))

def cpu():
    s1 = pygame.surface.Surface((largura_tela, 115))
    s1.fill(BRANCO)
    texto_cpu(s1, "Nome:", "brand_raw", 10)
    texto_cpu(s1, "Arquitetura:", "arch", 30)
    texto_cpu(s1, "Palavra (bits):", "bits", 50)
    texto_cpu(s1, "Frequência (MHz):", "freq", 70)
    texto_cpu(s1, "Núcleos (físicos):", "nucleos", 90)
    tela.blit(s1, (0, 100))

def uso_cpu():
    s = pygame.surface.Surface((largura_tela, altura_tela-250))
    s.fill(CINZA)
    l_cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2*y
    larg = (s.get_width()-2*y - (num_cpu+1)*desl)/num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, VERMELHO, (d, y, larg, alt))
        pygame.draw.rect(s, AZUL, 	(d, y, larg, (1-i/100)*alt))
        d = d + larg + desl
    mostra_texto("Uso da CPU por núcleo:", (512, 230), PRETO, cent=True, bold=True)
    # parte mais abaixo da tela e à esquerda
    tela.blit(s, (0, 250))

def rede():
    dic_interfaces = psutil.net_if_addrs()
    ip = dic_interfaces['Wi-Fi'][1].address
    text = f"Endereço IP:"
    mostra_texto(text,(20,120), PRETO, bold=True)
    text = f"{ip}"
    mostra_texto(text,(150,120), PRETO)

def mostra_conteudo(i):
    if i==0:
        cpu()
        uso_cpu()

    elif i==1:
        memoria()
        mostra_uso_disco()
        mostra_uso_memoria()

    elif i==2:
        rede()

    elif i==3:
        arquivos()
    
    else:
        processos()


terminou = False
i=1
while not terminou:
    abas = desenha_abas()
    mostra_texto("Projeto de Bloco", (512, 70), PRETO, cent=True, bold=True)
    mostra_conteudo(i)


    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for index, aba in enumerate(abas):
                    if aba.collidepoint(pos):
                        if index==0:
                            i=0
                        elif index==1:
                            i=1
                        elif index==2:
                            i=2
                        elif index==3:
                            i=3
                        else:
                            i=4

    pygame.display.update()
    tela.fill(BRANCO)
pygame.display.quit()
pygame.quit()