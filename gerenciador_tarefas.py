import pygame
from pygame import KEYDOWN
import psutil
import cpuinfo
import os
import time
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from matplotlib.figure import Figure


BRANCO = (255,255,255)
PRETO = (0,0,0)
LARANJA = (246,130,0)
VERMELHO = (230,0,0)
AZUL = (0,0,255)
CINZA = (200, 200, 200)

pygame.init()
pygame.display.set_caption("Gerenciador de Tarefas")
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

def sizedir(caminho, dir):
    p = os.path.join(caminho, dir)
    total = 0
    l2 = os.listdir(p)
    for a in l2:
        if os.path.isfile(os.path.join(p,a)):
            total += os.stat(p+'\\'+a).st_size
        if os.path.isdir(os.path.join(p,a)):
            total += sizedir(p,a)
    return total

def arquivos(path):
    path = r"{}".format(path)
    lista = os.listdir(path)
    dic = {}
    dic2={}
    for i in lista:
        if os.path.isfile((os.path.join(path,i))):
            dic[i] = []
            dic[i].append(os.stat(path +'\\'+i).st_size) # Tamanho
            dic[i].append(os.stat(path+'\\'+i).st_ctime) # Tempo de criação
        if os.path.isdir((os.path.join(path,i))):
            total = sizedir(path,i)
            dic2[i+' <DIR>'] = []
            dic2[i+' <DIR>'].append(total)
            dic2[i+' <DIR>'].append(os.stat(path+'\\'+i).st_mtime) # Tempo de criação

    texto = "Tamanho"
    mostra_texto(texto, (20, 100), PRETO, bold=True)
    texto = "Data de Modificação"
    mostra_texto(texto, (220, 100), PRETO, bold=True)
    texto = "Nome"
    mostra_texto(texto, (520, 100), PRETO, bold=True)

    y=130
    for i in dic2:
        kb = dic2[i][0]/1000
        if kb > 1000:
            mb = kb/1000
            texto = f'{mb:.2f} MB'
        else:
            texto = f'{kb:.2f} KB'
        mostra_texto(texto, (20, y), PRETO)
        dia = time.ctime(dic2[i][1])
        mostra_texto(dia, (220, y), PRETO)
        texto = i
        mostra_texto(i, (520, y), PRETO)
        y = y+30
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

def processos(pg):
    texto = "PID"
    mostra_texto(texto, (20, 80), PRETO, bold=True)
    texto = "# Threads"
    mostra_texto(texto, (120, 80), PRETO, bold=True)
    texto = "T. Usu."
    mostra_texto(texto, (290, 80), PRETO, bold=True)
    texto = "T. Sis."
    mostra_texto(texto, (460, 80), PRETO, bold=True)
    texto = "Mem.(%)"
    mostra_texto(texto, (630, 80), PRETO, bold=True)
    texto = "Executável"
    mostra_texto(texto, (800, 80), PRETO, bold=True)
    lista = psutil.pids()
    y = 110

    if pg == 1:
        lista = lista[:15]
    else:
        last = pg * 15
        init = last-15
        lista = lista[init:last]
    for i in lista:
        info_proc(i, y)
        y = y + 30

    pygame.draw.circle(tela, PRETO, (480, 580), 13, 2)
    pygame.draw.circle(tela, PRETO, (520, 580), 13, 2)
    pygame.draw.polygon(tela, PRETO, [(472, 580), (483, 572), (483, 588)])
    pygame.draw.polygon(tela, PRETO, [(528, 580), (517, 572), (517, 588)])

def memoria():
    disco = psutil.disk_usage('.')
    text = f"Total:"
    mostra_texto(text,(20,80), PRETO, bold=True)
    text = f"{format_memory(disco.total)} GB"
    mostra_texto(text,(120,80), PRETO)
    text = f"Em uso:"
    mostra_texto(text,(20,100), PRETO, bold=True)
    text = f"{format_memory(disco.used)} GB"
    mostra_texto(text,(120,100), PRETO)
    text = f"Livre:"
    mostra_texto(text,(20,120), PRETO, bold=True)
    text = f"{format_memory(disco.free)} GB"
    mostra_texto(text,(120,120), PRETO)
    text = f"Percentual de Disco Usado:"
    mostra_texto(text,(20,160), PRETO, bold=True)
    text = f"{disco.percent:}%"
    mostra_texto(text,(280,160), PRETO)

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
    tela.blit(s1, (0, 70))
    mostra_texto("Uso de CPU por núcleo:", (512, 230), PRETO, cent=True, bold=True)
    barras = pygame.Rect(780, 215, 100,30)
    pygame.draw.rect(tela, PRETO, barras)
    mostra_texto("Barras",(830,230), BRANCO, cent=True, bold=True)
    graf = pygame.Rect(900, 215, 100,30)
    pygame.draw.rect(tela, PRETO, graf)
    mostra_texto("Gráfico",(950,230), BRANCO, cent=True, bold=True)
    return barras, graf

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
    # parte mais abaixo da tela e à esquerda
    tela.blit(s, (0, 250))

def redes():
    texto = "Interface:"
    mostra_texto(texto, (20, 80), PRETO, bold=True)
    interfaces = psutil.net_if_addrs()
    status = psutil.net_if_stats()
    io_status = psutil.net_io_counters(pernic=True)
    nomes = []
    for i in interfaces:
        nomes.append(str(i))

    y = 115
    for i in nomes:
        texto = f'{i}:'
        mostra_texto(texto, (100, y), PRETO, bold=True)
        y += 30
        y_2 = y
        texto = "Ativo:"
        mostra_texto(texto, (500, y_2), PRETO)
        texto = f"{status[i].isup}"
        mostra_texto(texto, (630, y_2), PRETO)

        y_2 += 20
        texto = "Velocidade:"
        mostra_texto(texto, (500, y_2), PRETO)
        texto = f"{status[i].speed} MB"
        mostra_texto(texto, (630, y_2), PRETO)

        text = f"Uso de dados:"
        mostra_texto(text,(750,(y+10)), PRETO)
        usage = (io_status[i].bytes_sent + io_status[i].bytes_recv)/1000/1000
        text = f"{round(usage,2)} MB"
        mostra_texto(text,(890,(y+10)), PRETO)

        for j in interfaces[i]:
            if str(j.family) == 'AddressFamily.AF_INET':
                texto = "Endereço IP:"
                mostra_texto(texto, (130, y), PRETO)
                texto = f"{j.address}"
                mostra_texto(texto, (300, y), PRETO)

                y+=20
                texto = "Máscara de rede:"
                mostra_texto(texto, (130, y), PRETO)
                texto = f"{j.netmask}"
                mostra_texto(texto, (300, y), PRETO)
                y += 30
                break

def welcome():
    cont = pygame.Rect(100, 100, 824, 400)
    pygame.draw.rect(tela, PRETO, cont, 3)
    mostra_texto("Projeto de Bloco em Python", (512, 210), PRETO, cent=True, bold=True)
    mostra_texto("Gerenciador de Tarefas", (512, 250), PRETO, cent=True, bold=True)
    mostra_texto("Bloco: Arquitetura de Computadores, Sistemas Operacionais e Redes", (512, 290), PRETO, cent=True, bold=True)
    mostra_texto("Grupo: Jean Oliveira, Nelson José, Rafaela Breves e Rafaela Oliveira", (512, 330), PRETO, cent=True, bold=True)
    mostra_texto("Professora: Thaís Viana", (512, 370), PRETO, cent=True, bold=True)

def desenha_grafico(d):
    x = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)
    fig = Figure(figsize=(5.8, 3.2), dpi=100)
    ax = fig.add_subplot()
    for n in range(len(d)):
        ax.plot(x, d[f'nuc{n}'])
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data

def grafico_cpu():
    screen = pygame.display.get_surface()
    dic_nucleos = {}
    nucleos = psutil.cpu_count()
    for n in range(nucleos):
        dic_nucleos[f"nuc{n}"] = []
    for i in range(10):
        cpuinfo = psutil.cpu_percent(interval=None, percpu=True)
        for j in range(len(cpuinfo)):
            dic_nucleos[f"nuc{j}"].append(cpuinfo[j])
        time.sleep(0.5)

    canvas, raw_data = desenha_grafico(dic_nucleos)
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (200, 240)) 
    mostra_texto("tempo(s)", (512, 580), PRETO, cent=True)


# Input aba arquivos
bsfont = pygame.font.SysFont('calibri', 22)
usertext = ''
inputt = pygame.Rect(120, 60, 300, 30)
cor = PRETO

def inpt(a):
    if a == True:
        mostra_texto("Caminho:", (20, 65), PRETO)
        pygame.draw.rect(tela, cor, inputt, 2)

#Paginação aba Processos
pg = 1
pg_down = pygame.Rect(470, 570, 20, 20)
pg_up = pygame.Rect(510, 570, 20, 20)

ativo = False #input arquivos
aba_arq = False #aba arquivos
enter = False #enter input arquivos
inicio = True #tela inicial
nuc_cpu = False #contagem uso cpu
terminou = False
while not terminou:
    abas = desenha_abas()
    if inicio:
        tela.fill(BRANCO)
        desenha_abas()
        welcome()
    inpt(aba_arq)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for index, aba in enumerate(abas):
                    if aba.collidepoint(pos):
                        inicio=False
                        aba_arq = False
                        tela.fill(BRANCO)
                        if index==0:
                            barras, graf = cpu()
                            nuc_cpu = True
                            
                        elif index==1:
                            memoria()
                            mostra_uso_disco()
                            mostra_uso_memoria()
                        elif index==2:
                            redes()
                        elif index==3:
                            aba_arq = True
                        else:
                            processos(pg)


                if nuc_cpu:
                    if barras.collidepoint(pos):
                        tela.fill(BRANCO)
                        cpu()
                        uso_cpu()
                    elif graf.collidepoint(pos):
                        tela.fill(BRANCO)
                        cpu()
                        grafico_cpu()

                if pg_down.collidepoint(pos):
                    pg -= 1
                    tela.fill(BRANCO)
                    processos(pg)
                if pg_up.collidepoint(pos):
                    pg += 1
                    tela.fill(BRANCO)
                    processos(pg)

                if inputt.collidepoint(pos):
                    ativo = True
                else:
                    ativo = False
                    
            elif event.type == KEYDOWN:
                enter = False
                if ativo == True:
                    if event.key == pygame.K_BACKSPACE:
                        usertext = usertext[:-1]
                    else:
                        usertext += event.unicode
                    if event.key == pygame.K_RETURN:
                        usertext = usertext[:-1]
                        enter = True


    if aba_arq:
        txtsf = bsfont.render(usertext, True, PRETO)
        tela.blit(txtsf, (inputt.x+5, inputt.y + 7))
    pygame.display.update()

    if ativo:
        tela.fill(BRANCO)
        if enter:
            arquivos(usertext)
        cor = CINZA
    else:
        cor=PRETO

pygame.display.quit()
pygame.quit()