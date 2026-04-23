package com.dmhxm.teaching.application.evaluate.norm;

import java.util.List;
import java.util.Map;

/**
 * PEP-3 常模对照表
 * 包含某个年龄段所有副测验的常模数据
 *
 * @author kiro
 * @date 2026/4/23
 */
public class Pep3NormTable {

    /** 起始月龄（含） */
    private final int ageMonthFrom;

    /** 结束月龄（含） */
    private final int ageMonthTo;

    /** 各副测验的常模数据，key 为副测验代码（CVP/EL/RL/FM/GM/VMI/AE/SR/CMB/CVB/PB/PSC/AB） */
    private final Map<String, List<Pep3NormEntry>> norms;

    public Pep3NormTable(int ageMonthFrom, int ageMonthTo, Map<String, List<Pep3NormEntry>> norms) {
        this.ageMonthFrom = ageMonthFrom;
        this.ageMonthTo = ageMonthTo;
        this.norms = norms;
    }

    public int getAgeMonthFrom() {
        return ageMonthFrom;
    }

    public int getAgeMonthTo() {
        return ageMonthTo;
    }

    public Map<String, List<Pep3NormEntry>> getNorms() {
        return norms;
    }
}
