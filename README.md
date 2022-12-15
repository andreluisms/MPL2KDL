# MPL2KDL

Dependencies: asdl library

How to run: python source-name.py

Em geral, o dono de um repositório não vai permitir que outros criem ramos ou atualizem ramos do repositório, então, para um contribuidor fazer um *pull request*, este deve fazer um fork, atualizar o fork e, no github, fazer o pull request baseado no fork (https://opensource.com/article/19/7/create-pull-request-github). 


## <a id="2022-12-01-173712" href="/home/fabio/Documentos/MPL2KDL-Andre/diario.md#2022-12-01-173712">2022-12-01-173712</a>

clonei o repositório com `git clone https://github.com/andreluisms/MPL2KDL.git`

<pre><font color="#33DA7A"><b>fabio@super</b></font>:<font color="#2A7BDE"><b>~/Github</b></font>$ git clone https://github.com/andreluisms/MPL2KDL.git
Cloning into &apos;MPL2KDL&apos;...
remote: Enumerating objects: 5546, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 5546 (delta 0), reused 9 (delta 0), pack-reused 5537
Receiving objects: 100% (5546/5546), 196.20 MiB | 10.73 MiB/s, done.
Resolving deltas: 100% (1877/1877), done.
Updating files: 100% (5593/5593), done.
</pre>

Tentei executar o programa do André, mas falta uma dependência:
	
<pre><font color="#33DA7A"><b>fabio@super</b></font>:<font color="#2A7BDE"><b>~/Github/MPL2KDL</b></font>$ python3 mpl2kdl.py 
Traceback (most recent call last):
  File &quot;/home/fabio/Github/MPL2KDL/mpl2kdl.py&quot;, line 1, in &lt;module&gt;
    from python2kdl import generate_ontology
  File &quot;/home/fabio/Github/MPL2KDL/python2kdl.py&quot;, line 2, in &lt;module&gt;
    from asdl import parse, VisitorBase
ModuleNotFoundError: No module named &apos;asdl&apos;
</pre>

Instalei asdl: `pip3 install asdl`

Agora executou sem erros.

Executei wsmt em sua pasta:

<pre><font color="#33DA7A"><b>fabio@super</b></font>:<font color="#2A7BDE"><b>~/Github/MPL2KDL/wsmt2.0</b></font>$ ./wsmt
Gtk-<font color="#33DA7A"><b>Message</b></font>: <font color="#12488B">17:55:34.039</font>: Failed to load module &quot;canberra-gtk-module&quot;

</pre>

A parte do vídeo sobre a carga dos arquivos no wsmt começa aos 13 minutos.

- Cria workspace;
- Cria projeto;
- Arrasta os arquivos para dentro do projeto;
- Clicar com o botão da direita sobre o nome do arquivo wsml que quer converter;
	- nesse mesmo menu dá para abrir o grafo no Visualizer.
- Selecionar o ítem ConverTo;
	- no exemplo, convere para RDFS;


