---
title: "Asynchronous Value Sequences"
subtitle: "Draft Proposal"
document: D0000R0
date: today
audience:
  - "SG1 - parallelism and concurrency"
author:
  - name: Kirk Shoop
    email: <kirk.shoop@gmail.com>
toc: true
---

Introduction
============

```plantuml
title Omits Connect & Start
caption sequence diagram for set_next()
autonumber
hide footbox
participant consumer as cnm
participant producer as pdc
participant transformer as trn
activate cnm
group connect/start sequence
activate trn
activate pdc
end
loop values 0..N
pdc --> trn : processValN = set_next(produceValN)
activate pdc
activate trn
trn --> cnm : consumeValN = set_next(transformValN)
activate cnm
group connect/start valueN
end
pdc --> trn : set_value(transformValNRcvr, ValN...)
trn --> cnm : set_value(consumeValNRcvr, transformValN...)
cnm --> pdc : set_value(produceValN+1Rcvr)
deactivate pdc
deactivate trn
deactivate cnm
end
group end sequence
pdc --> trn : set_value(transformRcvr)
trn --> cnm : set_value(consumeRcvr)
deactivate pdc
deactivate trn
end
deactivate cnm
```
