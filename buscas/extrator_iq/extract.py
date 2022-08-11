from buscas.extrator_iq.Iqoption import IqOption
# from Iqoption import IqOption
from datetime import datetime, timedelta



class ExtracToDjango:
    TIMES = [1, 5, 15]
    VELAS = {1:1460, 5:300, 15:100}
    DAYS_EXTRACT = 12


    def __init__(self, login, senha) -> None:
        self.iq = IqOption()
        self.iq.conect(login, senha)


    def setVariables(self):
        self.clock_init = 0
        self.clock_end = 12
        self.day_now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.day_before = self.day_now - timedelta(days=1)

    
    def getVelasOneMinute1(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, int(self.VELAS[time]//1.5), time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_now and hora>=self.clock_init and hora<=self.clock_end:
                datas.append(c)
        return datas


    def getVelasOneMinute2(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, int(self.VELAS[time]//1.5), time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before and hora==self.clock_end:
                datas.append(c)
        return datas


    def getVelasMinuteAll(self, par, time):
        values = self.iq.getManyVelas(par, self.VELAS[time] * self.DAYS_EXTRACT, time)
        return values

    def getVelasFiveMinute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def getVelas15Minute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def formattingToDatabase(self, datas, time_vela):
        lista = []
        for data in datas:
            date = datetime.strptime(data[0][:10], "%Y-%m-%d")
            direcao = 'CALL' if data[-1]==1 else 'SELL'
            hora = int(data[0][11:13])
            minuto = int(data[0][14:16])
            row = {'date':date, 'timeframe':time_vela, 'direc':direcao, 'hora':hora, 'minuto':minuto}
            lista.append(row)
        return lista

    def pipeline(self, tipo, par, time):
        tipos = {
        '1 2':self.getVelasOneMinute2, '1 1':self.getVelasOneMinute1, '5':self.getVelasFiveMinute, '15':self.getVelas15Minute,
        '1 all':self.getVelasMinuteAll, '5 all':self.getVelasMinuteAll, '15 all':self.getVelasMinuteAll
        }

        datas = tipos[tipo](par, time)
        print(f'     Get data {par}')
        datas = self.formattingToDatabase(datas, time)
        print(f'     Send data {par}')
        return datas



if __name__ == '__main__':
    iq = ExtracToDjango('edno28@hotmail.com', '99730755ed')
    pares = ['EURUSD','GBPCHF']
    for par in pares:
        datas = iq.pipeline('1 1', par, 15)

    # a = AnaltyChances()
    # par = 'GBPCHF'
    # hora=12
    # minuto = 15
    # timeframe = 15

    # datas = a.getDatas(par, hora, minuto, timeframe)
    # a.formatChance(datas)