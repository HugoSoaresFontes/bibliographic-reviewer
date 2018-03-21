from threading import Thread

class ThreadWithReturnValue(Thread):
    """Herda de Thread, só que modifica o método join() para retornar o resultado
    da chamada da função designada por target.

    Assim, você pode iniciar várias threads e resgatar o retorno de cada uma separadamente."""

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