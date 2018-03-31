from threading import Thread
from functools import reduce


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=None):
        Thread.__init__(self, group=group, target=target, name=name,
                        args=args, kwargs=kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


def dive(item, routes, starter_item=None):
    """Faz uma chamada recursiva de keys de um dicionário aninhado.
    @param item: lista/dicionario a ser recursivamente resgatado.
    @param routes: rota por onde seguir, composta pelos campos/indices separados
        por pontos. Os campos/índices puramente numericos serão convertidos para inteiro,
        como se fossem índices de lista.
        Se routes for uma lista, a funcao ira tentar sucessivamente as rotas da lista,
        ate que um funcione ou que acabe a lista.
    @param starter_item: proxy para permitir que o item original seja acessivel dentro
        da funcao mesmo com certo nivel de recursividade. Nao deve ser usado pelo usuario!

    @return o valor/objeto no final do resgate. Se houver algum erro ao longo do caminho,
        será retornada a string 'error:%s' % key que deu erro.

    Exemplo:
    a = {"lista":[1,2]}
    dive(a, "lista.1") ---> 2

    """
    if starter_item == None:
        # Starter item serve para poder resetar e tentar novamente do começo
        starter_item = item

    if isinstance(routes, str):
        routes = [routes]

    checkpoints = routes[0].split('.')
    next_checkpoint = checkpoints.pop(0)
    # Fazemos a modificacao da rota in-place.
    routes[0] = ".".join(checkpoints)

    if next_checkpoint.isdigit():
        next_checkpoint = int(next_checkpoint)
    try:
        content = item[next_checkpoint]
    except Exception as e:
        # Deu errado: joga essa rota que estavamos tentando fora
        routes.pop(0)
        if isinstance(routes, list) and len(routes):
            # Comeca do zero, na proxima rota, se tiver
            return dive(starter_item, routes)
        # Nao tem proxima rota, entao deu erro mesmo
        return "error:%s|%s<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" % (next_checkpoint, repr(e))

    if len(checkpoints) == 0:
        return content
    # Passa o terceiro argumento para poder saber como reiniciar se der erro
    return dive(content, routes, starter_item)


def deepgetter(obj, attrs, default=None):
    """Faz uma chamada sucessiva da função getattr, para ir pegando os atributos
    de um objeto.
    Exemplo:
    deepgetter(Cidade, 'regiao.pais') é equivalente a fazer Cidade.regiao.pais
    """
    getter = lambda x, y: getattr(x, y, default)
    return reduce(getter, attrs.split('.'), obj)


def inclusive_range(start, end, step=1):
    """Gerador que retorna tuplas que servirao para delimitar os retstart (offset de inicio do retorno da API)
    e o retmax (quantos artigos virao em cada requisicao).
    Serve para poder pegar todos os artigos em chunks, e é necessario pois
    não é possivel pegar varios artigos de uma vez por causa do erro HTTP 413 (request URI too large)

    Exemplo:
    inclusive_range(1,6,2)
    retorna:
    [(1,2),
     (3,2),
     (5,1)]
     Em cada tupla, o primeiro item é o offset de inicio e o segundo é o limite de retornos"""

    while start < end:
        tupla = None
        if start + step < end:
            tupla = (start, step)
            start = start + step
        else:
            tupla = (start, end - start)
            start = end

        yield tupla