package com.dmhxm.teaching.application.evaluate.norm;

/**
 * PEP-3 常模数据条目
 * 每条记录包含：原始分、标准分、百分等级
 *
 * @author kiro
 * @date 2026/4/23
 */
public class Pep3NormEntry {

    /** 原始分 */
    private final int rawScore;

    /** 标准分 */
    private final int standardScore;

    /** 百分等级（如 "13", "<6", ">99"） */
    private final String percentileRank;

    public Pep3NormEntry(int rawScore, int standardScore, String percentileRank) {
        this.rawScore = rawScore;
        this.standardScore = standardScore;
        this.percentileRank = percentileRank;
    }

    public int getRawScore() {
        return rawScore;
    }

    public int getStandardScore() {
        return standardScore;
    }

    public String getPercentileRank() {
        return percentileRank;
    }
}
