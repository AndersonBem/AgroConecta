USE AgroConecta;

-- ================= GESTOR =================
-- 8 registros
INSERT INTO Gestor (CPF, nome, email, senha_hash, usuario) VALUES
('001.001.001-01','Gestor 01','gestor01@agro.com','dev_hash','gestor01'),
('002.002.002-02','Gestor 02','gestor02@agro.com','dev_hash','gestor02'),
('003.003.003-03','Gestor 03','gestor03@agro.com','dev_hash','gestor03'),
('004.004.004-04','Gestor 04','gestor04@agro.com','dev_hash','gestor04'),
('005.005.005-05','Gestor 05','gestor05@agro.com','dev_hash','gestor05'),
('006.006.006-06','Gestor 06','gestor06@agro.com','dev_hash','gestor06'),
('007.007.007-07','Gestor 07','gestor07@agro.com','dev_hash','gestor07'),
('008.008.008-08','Gestor 08','gestor08@agro.com','dev_hash','gestor08');

-- ================= OPERADORARMAZEM =================
-- 8 registros
INSERT INTO OperadorArmazem (nome, email, senha_hash, usuario) VALUES
('Operador 01','operador01@agro.com','dev_hash','op01'),
('Operador 02','operador02@agro.com','dev_hash','op02'),
('Operador 03','operador03@agro.com','dev_hash','op03'),
('Operador 04','operador04@agro.com','dev_hash','op04'),
('Operador 05','operador05@agro.com','dev_hash','op05'),
('Operador 06','operador06@agro.com','dev_hash','op06'),
('Operador 07','operador07@agro.com','dev_hash','op07'),
('Operador 08','operador08@agro.com','dev_hash','op08');

-- ================= ENDERECO =================
-- 25 registros (idEndereco 1..25)
INSERT INTO Endereco (UF, cidade, bairro, rua, numero, comp, cep) VALUES
('PE','Caruaru','Centro','Rua das Sementes',100,'Galpao A','55000-000'),
('PE','Garanhuns','Boa Vista','Av. do Campo',105,'Galpao B','55290-000'),
('PE','Petrolina','Industrial','Estrada da Colheita',110,'Galpao C','56300-000'),
('PE','Recife','Rural','Rua do Milho',115,'Galpao D','50000-000'),
('PE','Serra Talhada','Nova Esperanca','Travessa da Safra',120,'Galpao E','56900-000'),
('PE','Caruaru','Centro','Rua das Sementes',125,'Galpao A','55000-000'),
('PE','Garanhuns','Boa Vista','Av. do Campo',130,'Galpao B','55290-000'),
('PE','Petrolina','Industrial','Estrada da Colheita',135,'Galpao C','56300-000'),
('PE','Recife','Rural','Rua do Milho',140,'Galpao D','50000-000'),
('PE','Serra Talhada','Nova Esperanca','Travessa da Safra',145,'Galpao E','56900-000'),
('PE','Caruaru','Centro','Rua das Sementes',150,'Galpao A','55000-000'),
('PE','Garanhuns','Boa Vista','Av. do Campo',155,'Galpao B','55290-000'),
('PE','Petrolina','Industrial','Estrada da Colheita',160,'Galpao C','56300-000'),
('PE','Recife','Rural','Rua do Milho',165,'Galpao D','50000-000'),
('PE','Serra Talhada','Nova Esperanca','Travessa da Safra',170,'Galpao E','56900-000'),
('PE','Caruaru','Centro','Rua das Sementes',175,'Galpao A','55000-000'),
('PE','Garanhuns','Boa Vista','Av. do Campo',180,'Galpao B','55290-000'),
('PE','Petrolina','Industrial','Estrada da Colheita',185,'Galpao C','56300-000'),
('PE','Recife','Rural','Rua do Milho',190,'Galpao D','50000-000'),
('PE','Serra Talhada','Nova Esperanca','Travessa da Safra',195,'Galpao E','56900-000'),
('PE','Caruaru','Centro','Rua das Sementes',200,'Galpao A','55000-000'),
('PE','Garanhuns','Boa Vista','Av. do Campo',205,'Galpao B','55290-000'),
('PE','Petrolina','Industrial','Estrada da Colheita',210,'Galpao C','56300-000'),
('PE','Recife','Rural','Rua do Milho',215,'Galpao D','50000-000'),
('PE','Serra Talhada','Nova Esperanca','Travessa da Safra',220,'Galpao E','56900-000');

-- ================= TIPOSEMENTE =================
-- 8 registros
INSERT INTO TipoSemente (nome, descricao) VALUES
('Milho Hibrido','Milho hibrido de alta produtividade'),
('Feijao Carioca','Feijao carioca para inverno'),
('Soja Intacta','Soja resistente a pragas'),
('Arroz Irrigado','Arroz para areas irrigadas'),
('Sorgo Forrageiro','Sorgo para alimentacao animal'),
('Trigo','Trigo para farinha'),
('Algodao','Algodao para fibra'),
('Girassol','Girassol para oleo vegetal');

-- ================= SAFRA =================
-- 6 registros
INSERT INTO Safra (ano, descricao) VALUES
('2024-01-01','Safra 1'),
('2024-07-01','Safra 2'),
('2025-01-01','Safra 3'),
('2025-07-01','Safra 4'),
('2026-01-01','Safra 5'),
('2026-07-01','Safra 6');

-- ================= STATUS =================
-- 4 registros
INSERT INTO Status (nome, descricao) VALUES
('Pendente','Solicitacao aguardando analise'),
('Aprovada','Solicitacao aprovada'),
('Reprovada','Solicitacao reprovada'),
('Cancelada','Solicitacao cancelada pela cooperativa');

-- ================= COOPERATIVA =================
-- 12 registros (usando Endereco 1..12)
INSERT INTO Cooperativa (CNPJ, razaoSocial, nomeResponsavel, cpfResponsavel, emailInstitucional, senha_hash, usuario, Endereco_idEndereco) VALUES
('12.345.678/0001','Cooperativa Agro 01','Responsavel Coop 01','999.888.7701','coop01@agro.com','dev_hash','coop01',1),
('12.345.678/0002','Cooperativa Agro 02','Responsavel Coop 02','999.888.7702','coop02@agro.com','dev_hash','coop02',2),
('12.345.678/0003','Cooperativa Agro 03','Responsavel Coop 03','999.888.7703','coop03@agro.com','dev_hash','coop03',3),
('12.345.678/0004','Cooperativa Agro 04','Responsavel Coop 04','999.888.7704','coop04@agro.com','dev_hash','coop04',4),
('12.345.678/0005','Cooperativa Agro 05','Responsavel Coop 05','999.888.7705','coop05@agro.com','dev_hash','coop05',5),
('12.345.678/0006','Cooperativa Agro 06','Responsavel Coop 06','999.888.7706','coop06@agro.com','dev_hash','coop06',6),
('12.345.678/0007','Cooperativa Agro 07','Responsavel Coop 07','999.888.7707','coop07@agro.com','dev_hash','coop07',7),
('12.345.678/0008','Cooperativa Agro 08','Responsavel Coop 08','999.888.7708','coop08@agro.com','dev_hash','coop08',8),
('12.345.678/0009','Cooperativa Agro 09','Responsavel Coop 09','999.888.7709','coop09@agro.com','dev_hash','coop09',9),
('12.345.678/0010','Cooperativa Agro 10','Responsavel Coop 10','999.888.7710','coop10@agro.com','dev_hash','coop10',10),
('12.345.678/0011','Cooperativa Agro 11','Responsavel Coop 11','999.888.7711','coop11@agro.com','dev_hash','coop11',11),
('12.345.678/0012','Cooperativa Agro 12','Responsavel Coop 12','999.888.7712','coop12@agro.com','dev_hash','coop12',12);

-- ================= TELEFONE =================
-- 30 registros (8 gestores + 12 coops + 10 extras)
INSERT INTO Telefone (numero, Gestor_CPF, Cooperativa_CNPJ) VALUES
('(81) 9001-0000','001.001.001-01',NULL),
('(81) 9002-0000','002.002.002-02',NULL),
('(81) 9003-0000','003.003.003-03',NULL),
('(81) 9004-0000','004.004.004-04',NULL),
('(81) 9005-0000','005.005.005-05',NULL),
('(81) 9006-0000','006.006.006-06',NULL),
('(81) 9007-0000','007.007.007-07',NULL),
('(81) 9008-0000','008.008.008-08',NULL),

('(81) 9101-1111',NULL,'12.345.678/0001'),
('(81) 9102-1111',NULL,'12.345.678/0002'),
('(81) 9103-1111',NULL,'12.345.678/0003'),
('(81) 9104-1111',NULL,'12.345.678/0004'),
('(81) 9105-1111',NULL,'12.345.678/0005'),
('(81) 9106-1111',NULL,'12.345.678/0006'),
('(81) 9107-1111',NULL,'12.345.678/0007'),
('(81) 9108-1111',NULL,'12.345.678/0008'),
('(81) 9109-1111',NULL,'12.345.678/0009'),
('(81) 9110-1111',NULL,'12.345.678/0010'),
('(81) 9111-1111',NULL,'12.345.678/0011'),
('(81) 9112-1111',NULL,'12.345.678/0012'),

('(81) 9201-2222',NULL,'12.345.678/0001'),
('(81) 9202-2222',NULL,'12.345.678/0003'),
('(81) 9203-2222',NULL,'12.345.678/0005'),
('(81) 9204-2222',NULL,'12.345.678/0007'),
('(81) 9205-2222',NULL,'12.345.678/0009'),
('(81) 9206-2222',NULL,'12.345.678/0011'),
('(81) 9207-2222',NULL,'12.345.678/0002'),
('(81) 9208-2222',NULL,'12.345.678/0004'),
('(81) 9209-2222',NULL,'12.345.678/0006'),
('(81) 9210-2222',NULL,'12.345.678/0008');

-- ================= ARMAZEM =================
-- 20 registros (usa Gestor, Endereco 13..25, Operador 1..8)
INSERT INTO Armazem (nome, descricao, Gestor_CPF, Endereco_idEndereco, OperadorArmazem_idOperadorArmazem) VALUES
('Armazem 01','Armazem regional 01','001.001.001-01',13,1),
('Armazem 02','Armazem regional 02','002.002.002-02',14,2),
('Armazem 03','Armazem regional 03','003.003.003-03',15,3),
('Armazem 04','Armazem regional 04','004.004.004-04',16,4),
('Armazem 05','Armazem regional 05','005.005.005-05',17,5),
('Armazem 06','Armazem regional 06','006.006.006-06',18,6),
('Armazem 07','Armazem regional 07','007.007.007-07',19,7),
('Armazem 08','Armazem regional 08','008.008.008-08',20,8),
('Armazem 09','Armazem regional 09','001.001.001-01',21,1),
('Armazem 10','Armazem regional 10','002.002.002-02',22,2),
('Armazem 11','Armazem regional 11','003.003.003-03',23,3),
('Armazem 12','Armazem regional 12','004.004.004-04',24,4),
('Armazem 13','Armazem regional 13','005.005.005-05',25,5),
('Armazem 14','Armazem regional 14','006.006.006-06',13,6),
('Armazem 15','Armazem regional 15','007.007.007-07',14,7),
('Armazem 16','Armazem regional 16','008.008.008-08',15,8),
('Armazem 17','Armazem regional 17','001.001.001-01',16,1),
('Armazem 18','Armazem regional 18','002.002.002-02',17,2),
('Armazem 19','Armazem regional 19','003.003.003-03',18,3),
('Armazem 20','Armazem regional 20','004.004.004-04',19,4);

-- ================= LOTE =================
-- 40 registros (rodando Armazem 1..20 e TipoSemente 1..8)
INSERT INTO Lote (dataEntrada, dataVencimento, dataSaida, peso, Armazem_idArmazem, TipoSemente_idTipoSemente, qr_payload, Lotecol) VALUES
('2025-05-02','2025-12-31',NULL,1050,1,1,'QR0001','Lote-001'),
('2025-06-03','2025-12-31',NULL,1100,2,2,'QR0002','Lote-002'),
('2025-07-04','2025-12-31',NULL,1150,3,3,'QR0003','Lote-003'),
('2025-10-05','2025-12-31',NULL,1200,4,4,'QR0004','Lote-004'),
('2025-11-06','2025-12-31',NULL,1250,5,5,'QR0005','Lote-005'),
('2025-08-07','2025-12-31',NULL,1300,6,6,'QR0006','Lote-006'),
('2025-09-08','2025-12-31',NULL,1350,7,7,'QR0007','Lote-007'),
('2025-10-09','2025-12-31',NULL,1400,8,8,'QR0008','Lote-008'),
('2025-06-10','2025-12-31',NULL,1450,9,1,'QR0009','Lote-009'),
('2025-05-11','2025-12-31',NULL,1500,10,2,'QR0010','Lote-010'),
('2025-05-12','2025-12-31',NULL,1550,11,3,'QR0011','Lote-011'),
('2025-06-13','2025-12-31',NULL,1600,12,4,'QR0012','Lote-012'),
('2025-07-14','2025-12-31',NULL,1650,13,5,'QR0013','Lote-013'),
('2025-08-15','2025-12-31',NULL,1700,14,6,'QR0014','Lote-014'),
('2025-09-16','2025-12-31',NULL,1750,15,7,'QR0015','Lote-015'),
('2025-10-17','2025-12-31',NULL,1800,16,8,'QR0016','Lote-016'),
('2025-11-18','2025-12-31',NULL,1850,17,1,'QR0017','Lote-017'),
('2025-09-19','2025-12-31',NULL,1900,18,2,'QR0018','Lote-018'),
('2025-08-20','2025-12-31',NULL,1950,19,3,'QR0019','Lote-019'),
('2025-07-21','2025-12-31',NULL,2000,20,4,'QR0020','Lote-020'),
('2025-06-22','2025-12-31',NULL,2050,1,5,'QR0021','Lote-021'),
('2025-05-23','2025-12-31',NULL,2100,2,6,'QR0022','Lote-022'),
('2025-04-24','2025-12-31',NULL,2150,3,7,'QR0023','Lote-023'),
('2025-03-25','2025-12-31',NULL,2200,4,8,'QR0024','Lote-024'),
('2025-04-26','2025-12-31',NULL,2250,5,1,'QR0025','Lote-025'),
('2025-11-27','2025-12-31',NULL,2300,6,2,'QR0026','Lote-026'),
('2025-10-28','2025-12-31',NULL,2350,7,3,'QR0027','Lote-027'),
('2025-08-01','2025-12-31',NULL,2400,8,4,'QR0028','Lote-028'),
('2025-09-02','2025-12-31',NULL,2450,9,5,'QR0029','Lote-029'),
('2025-07-03','2025-12-31',NULL,2500,10,6,'QR0030','Lote-030'),
('2025-06-04','2025-12-31',NULL,2550,11,7,'QR0031','Lote-031'),
('2025-05-05','2025-12-31',NULL,2600,12,8,'QR0032','Lote-032'),
('2025-06-06','2025-12-31',NULL,2650,13,1,'QR0033','Lote-033'),
('2025-07-07','2025-12-31',NULL,2700,14,2,'QR0034','Lote-034'),
('2025-08-08','2025-12-31',NULL,2750,15,3,'QR0035','Lote-035'),
('2025-09-09','2025-12-31',NULL,2800,16,4,'QR0036','Lote-036'),
('2025-10-10','2025-12-31',NULL,2850,17,5,'QR0037','Lote-037'),
('2025-05-11','2025-12-31',NULL,2900,18,6,'QR0038','Lote-038'),
('2025-06-12','2025-12-31',NULL,2950,19,7,'QR0039','Lote-039'),
('2025-07-13','2025-12-31',NULL,3000,20,8,'QR0040','Lote-040');

-- ================= SOLICITACAO =================
-- 35 registros (coops 1..12, safra 1..6, status 1..4)
INSERT INTO Solicitacao (quantidade, numeroProdutoresBeneficiados, observacao, Cooperativa_CNPJ, Safra_idSafra, Status_idStatus) VALUES
(1100,11,'Solicitacao 01 para distribuicao de sementes','12.345.678/0001',1,1),
(1200,12,'Solicitacao 02 para distribuicao de sementes','12.345.678/0002',2,2),
(1300,13,'Solicitacao 03 para distribuicao de sementes','12.345.678/0003',3,3),
(1400,14,'Solicitacao 04 para distribuicao de sementes','12.345.678/0004',4,4),
(1500,15,'Solicitacao 05 para distribuicao de sementes','12.345.678/0005',5,1),
(1600,16,'Solicitacao 06 para distribuicao de sementes','12.345.678/0006',6,2),
(1700,17,'Solicitacao 07 para distribuicao de sementes','12.345.678/0007',1,3),
(1800,18,'Solicitacao 08 para distribuicao de sementes','12.345.678/0008',2,4),
(1900,19,'Solicitacao 09 para distribuicao de sementes','12.345.678/0009',3,1),
(2000,20,'Solicitacao 10 para distribuicao de sementes','12.345.678/0010',4,2),
(2100,21,'Solicitacao 11 para distribuicao de sementes','12.345.678/0011',5,3),
(2200,22,'Solicitacao 12 para distribuicao de sementes','12.345.678/0012',6,4),
(2300,23,'Solicitacao 13 para distribuicao de sementes','12.345.678/0001',1,1),
(2400,24,'Solicitacao 14 para distribuicao de sementes','12.345.678/0002',2,2),
(2500,25,'Solicitacao 15 para distribuicao de sementes','12.345.678/0003',3,3),
(2600,26,'Solicitacao 16 para distribuicao de sementes','12.345.678/0004',4,4),
(2700,27,'Solicitacao 17 para distribuicao de sementes','12.345.678/0005',5,1),
(2800,28,'Solicitacao 18 para distribuicao de sementes','12.345.678/0006',6,2),
(2900,29,'Solicitacao 19 para distribuicao de sementes','12.345.678/0007',1,3),
(3000,30,'Solicitacao 20 para distribuicao de sementes','12.345.678/0008',2,4),
(3100,11,'Solicitacao 21 para distribuicao de sementes','12.345.678/0009',3,1),
(3200,12,'Solicitacao 22 para distribuicao de sementes','12.345.678/0010',4,2),
(3300,13,'Solicitacao 23 para distribuicao de sementes','12.345.678/0011',5,3),
(3400,14,'Solicitacao 24 para distribuicao de sementes','12.345.678/0012',6,4),
(3500,15,'Solicitacao 25 para distribuicao de sementes','12.345.678/0001',1,1),
(3600,16,'Solicitacao 26 para distribuicao de sementes','12.345.678/0002',2,2),
(3700,17,'Solicitacao 27 para distribuicao de sementes','12.345.678/0003',3,3),
(3800,18,'Solicitacao 28 para distribuicao de sementes','12.345.678/0004',4,4),
(3900,19,'Solicitacao 29 para distribuicao de sementes','12.345.678/0005',5,1),
(4000,20,'Solicitacao 30 para distribuicao de sementes','12.345.678/0006',6,2),
(4100,21,'Solicitacao 31 para distribuicao de sementes','12.345.678/0007',1,3),
(4200,22,'Solicitacao 32 para distribuicao de sementes','12.345.678/0008',2,4),
(4300,23,'Solicitacao 33 para distribuicao de sementes','12.345.678/0009',3,1),
(4400,24,'Solicitacao 34 para distribuicao de sementes','12.345.678/0010',4,2),
(4500,25,'Solicitacao 35 para distribuicao de sementes','12.345.678/0011',5,3);

-- ================= SOLICITACAOTIPOSEMENTE =================
-- 44 registros (várias sementes por solicitacao)
INSERT INTO SolicitacaoTipoSemente (Solicitacao_idSolicitacao, TipoSemente_idTipoSemente, quantidade) VALUES
(1,1,250),
(1,2,300),
(2,3,350),
(2,4,400),
(3,5,450),
(3,6,500),
(4,7,550),
(4,8,600),
(5,1,650),
(5,2,700),
(6,3,750),
(6,4,800),
(7,5,850),
(7,6,900),
(8,7,950),
(8,8,1000),
(9,1,1050),
(9,2,1100),
(10,3,1150),
(10,4,1200),
(11,5,1250),
(11,6,1300),
(12,7,1350),
(12,8,1400),
(13,1,1450),
(14,2,1500),
(15,3,1550),
(16,4,1600),
(17,5,1650),
(18,6,1700),
(19,7,1750),
(20,8,1800),
(21,1,1850),
(22,2,1900),
(23,3,1950),
(24,4,2000),
(25,5,2050),
(26,6,2100),
(27,7,2150),
(28,8,2200),
(29,1,2250),
(30,2,2300),
(31,3,2350),
(32,4,2400);


SET @senha := 'pbkdf2_sha256$1000000$1eUagG34tgiPuhD5bNOAp0$P91I72DRe43Bz/pnk7cfrA62i/TKpLqyP9KJIJeG/VU=';
SET SQL_SAFE_UPDATES = 0;
UPDATE Gestor
SET senha_hash = @senha;

UPDATE Cooperativa
SET senha_hash = @senha;

UPDATE OperadorArmazem
SET senha_hash = @senha;
SET SQL_SAFE_UPDATES = 1;