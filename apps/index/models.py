# apps/index/models.py
from django.db import models

class Gestor(models.Model):
    cpf = models.CharField(db_column='CPF', primary_key=True, max_length=14)
    nome = models.CharField(max_length=60)
    email = models.CharField(max_length=80)
    senha_hash = models.CharField(db_column='senha_hash', max_length=128)
    usuario = models.CharField(db_column='usuario', max_length=20)
    class Meta:
        managed = False
        db_table = 'Gestor'

class Endereco(models.Model):
    idendereco = models.AutoField(db_column='idEndereco', primary_key=True)
    uf = models.CharField(db_column='UF', max_length=2)
    cidade = models.CharField(max_length=45)
    bairro = models.CharField(max_length=45)
    rua = models.CharField(max_length=45)
    numero = models.IntegerField()
    comp = models.CharField(max_length=45, blank=True, null=True)
    cep = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'Endereco'

class OperadorArmazem(models.Model):
    idoperadorarmazem = models.AutoField(db_column='idOperadorArmazem', primary_key=True)
    nome = models.CharField(max_length=60)
    email = models.CharField(max_length=80)
    senha_hash = models.CharField(db_column='senha_hash', max_length=128)
    usuario = models.CharField(db_column='usuario', max_length=20)

    class Meta:
        managed = False
        db_table = 'OperadorArmazem'

class Armazem(models.Model):
    idarmazem = models.AutoField(db_column='idArmazem', primary_key=True)
    nome = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150, blank=True, null=True)
    gestor_cpf = models.ForeignKey(
        Gestor, models.DO_NOTHING,
        db_column='Gestor_CPF'
    )
    endereco_idendereco = models.ForeignKey(
        Endereco, models.DO_NOTHING,
        db_column='Endereco_idEndereco'
    )
    operadorarmazem_idoperadorarmazem = models.ForeignKey(
        OperadorArmazem, models.DO_NOTHING,
        db_column='OperadorArmazem_idOperadorArmazem',
        blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'Armazem'

class Cooperativa(models.Model):
    cnpj = models.CharField(db_column='CNPJ', primary_key=True, max_length=18)
    razaosocial = models.CharField(db_column='razaoSocial', max_length=60)
    nomeresponsavel = models.CharField(db_column='nomeResponsavel', max_length=60)
    cpfresponsavel = models.CharField(db_column='cpfResponsavel', max_length=14, blank=True, null=True)
    emailinstitucional = models.CharField(db_column='emailInstitucional', max_length=80, unique=True)
    senha_hash = models.CharField(db_column='senha_hash', max_length=128)
    usuario = models.CharField(db_column='usuario', max_length=20)
    endereco_idendereco = models.ForeignKey(
        Endereco, models.DO_NOTHING,
        db_column='Endereco_idEndereco'
    )

    class Meta:
        managed = False
        db_table = 'Cooperativa'

class Telefone(models.Model):
    idtelefone = models.AutoField(db_column='idTelefone', primary_key=True)
    numero = models.CharField(max_length=15, blank=True, null=True)
    gestor_cpf = models.ForeignKey(
        Gestor, models.CASCADE,
        db_column='Gestor_CPF', blank=True, null=True
    )
    cooperativa_cnpj = models.ForeignKey(
        Cooperativa, models.CASCADE,
        db_column='Cooperativa_CNPJ', blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'Telefone'

class TipoSemente(models.Model):
    idtiposemente = models.AutoField(db_column='idTipoSemente', primary_key=True)
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TipoSemente'

class Lote(models.Model):
    idlote = models.AutoField(db_column='idLote', primary_key=True)
    dataentrada = models.DateField(db_column='dataEntrada')
    datavencimento = models.DateField(db_column='dataVencimento')
    datasaida = models.DateTimeField(db_column='dataSaida', blank=True, null=True)
    peso = models.PositiveIntegerField()
    armazem_idarmazem = models.ForeignKey(
        Armazem, models.DO_NOTHING,
        db_column='Armazem_idArmazem'
    )
    tiposemente_idtiposemente = models.ForeignKey(
        TipoSemente, models.DO_NOTHING,
        db_column='TipoSemente_idTipoSemente'
    )
    qr_payload = models.CharField(max_length=255, blank=True, null=True)
    lotecol = models.CharField(db_column='Lotecol', max_length=45)

    class Meta:
        managed = False
        db_table = 'Lote'

class Safra(models.Model):
    idsafra = models.AutoField(db_column='idSafra', primary_key=True)
    ano = models.DateField()  # veio como DATE no script
    descricao = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Safra'

class Status(models.Model):
    idstatus = models.AutoField(db_column='idStatus', primary_key=True)
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Status'

class Solicitacao(models.Model):
    idsolicitacao = models.AutoField(db_column='idSolicitacao', primary_key=True)
    quantidade = models.PositiveIntegerField()
    numeroprodutoresbeneficiados = models.PositiveIntegerField(db_column='numeroProdutoresBeneficiados')
    observacao = models.CharField(max_length=150, blank=True, null=True)
    cooperativa_cnpj = models.ForeignKey(
        Cooperativa, models.CASCADE,
        db_column='Cooperativa_CNPJ'
    )
    safra_idsafra = models.ForeignKey(
        Safra, models.DO_NOTHING,
        db_column='Safra_idSafra'
    )
    status_idstatus = models.ForeignKey(
        Status, models.DO_NOTHING,
        db_column='Status_idStatus'
    )

    class Meta:
        managed = False
        db_table = 'Solicitacao'

# Tabela de associação (PK composta no MySQL)
class SolicitacaoTipoSemente(models.Model):
    
    solicitacao_idsolicitacao = models.ForeignKey(
        Solicitacao,
        models.CASCADE,
        db_column='Solicitacao_idSolicitacao',
        primary_key=True,
    )
    tiposemente_idtiposemente = models.ForeignKey(
        TipoSemente,
        models.CASCADE,
        db_column='TipoSemente_idTipoSemente',
    )
    quantidade = models.PositiveIntegerField()

    class Meta:
        managed = False              
        db_table = 'SolicitacaoTipoSemente'
        unique_together = (          
            ('solicitacao_idsolicitacao', 'tiposemente_idtiposemente'),
        )
