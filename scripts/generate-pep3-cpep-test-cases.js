const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];

    if (inQuotes) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        field += ch;
      }
      continue;
    }

    if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (ch !== '\r') {
      field += ch;
    }
  }

  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  const headers = rows.shift();
  return rows
    .filter((r) => r.some((v) => String(v || '').trim() !== ''))
    .map((r) => Object.fromEntries(headers.map((h, idx) => [h, r[idx] || ''])));
}

function readCsv(relPath) {
  return parseCsv(fs.readFileSync(path.join(ROOT, relPath), 'utf8'));
}

function buildOptions(row) {
  const letters = ['a', 'b', 'c', 'd', 'e'];
  const options = {};

  letters.forEach((letter) => {
    const value = row[`评分_${letter}_分值`];
    const label = row[`评分_${letter}_标签`];
    const description = row[`评分_${letter}_说明`];
    if (value !== '' || label !== '' || description !== '') {
      options[letter] = { value: String(value), label, description };
    }
  });

  return options;
}

function optionKeyForScore(options, score, preferredLabels = []) {
  const entries = Object.entries(options);
  const sameScore = entries.filter(([, option]) => Number(option.value) === score);
  if (sameScore.length === 0) {
    return entries[0] ? entries[0][0] : 'a';
  }

  for (const preferred of preferredLabels) {
    const found = sameScore.find(([, option]) => option.label.includes(preferred));
    if (found) return found[0];
  }

  const nonNa = sameScore.find(([, option]) => !/NA|不适用/i.test(option.label));
  return (nonNa || sameScore[0])[0];
}

function summarizeByDomain(answers, categoryFilter, scoreLabels) {
  const result = {};

  answers
    .filter((answer) => categoryFilter(answer))
    .forEach((answer) => {
      const key = answer.category2;
      if (!result[key]) {
        result[key] = {
          total: 0,
          scoreTotal: 0,
          counts: Object.fromEntries(scoreLabels.map((label) => [label, 0])),
        };
      }
      result[key].total += 1;
      result[key].scoreTotal += Number(answer.score) || 0;
      if (answer.selectedLabel in result[key].counts) {
        result[key].counts[answer.selectedLabel] += 1;
      }
    });

  return result;
}

function chooseFromPattern(indexInDomain, counts, values) {
  const expanded = [];
  values.forEach((value) => {
    for (let i = 0; i < (counts[value] || 0); i += 1) expanded.push(value);
  });
  if (expanded.length === 0) return values[0];
  return expanded[indexInDomain % expanded.length];
}

function makePep3Case() {
  const rows = readCsv('data/pep3-config-v5.csv');
  const domainIndex = {};

  const developmentTargets = {
    '认知(语言/语前)-CVP': { 2: 15, 1: 8, 0: 11 },
    '语言表达-EL': { 2: 7, 1: 8, 0: 10 },
    '语言理解-RL': { 2: 6, 1: 5, 0: 8 },
    '小肌肉-FM': { 2: 16, 1: 3, 0: 1 },
    '大肌肉-GM': { 2: 11, 1: 3, 0: 1 },
    '模仿(视觉/动作)-VMI': { 2: 8, 1: 1, 0: 1 },
  };
  const behaviorTargets = {
    '情感表达-AE': { 2: 6, 1: 3, 0: 2 },
    '社交互动-SR': { 2: 4, 1: 5, 0: 3 },
    '行为特征-非语言-CMB': { 2: 8, 1: 4, 0: 3 },
    '行为特征-语言-CVB': { 2: 3, 1: 4, 0: 4 },
  };
  const notes = [
    '需要多次示范后才能进入任务',
    '对泡泡、拼图和积木材料兴趣较高',
    '口语回应较少，多以手势或拿取表达需要',
    '转换任务时有短暂抗拒，视觉提示后可继续',
    '在精细操作任务中配合度较好',
    '听觉指令需要重复或结合手势提示',
  ];

  const answers = rows.map((row, idx) => {
    const domain = row['二级分类'];
    domainIndex[domain] = domainIndex[domain] || 0;
    const withinDomain = domainIndex[domain];
    domainIndex[domain] += 1;

    let score = 2;
    let preferredLabels = ['通过', '恰当', '没有出现', '是', '轻微', '3-4岁'];

    if (row['一级分类'] === '发展副测验') {
      score = chooseFromPattern(withinDomain, developmentTargets[domain], [2, 1, 0]);
      preferredLabels = score === 2 ? ['通过'] : score === 1 ? ['萌芽'] : ['不通过'];
    } else if (row['一级分类'] === '行为副测验') {
      score = chooseFromPattern(withinDomain, behaviorTargets[domain], [2, 1, 0]);
      preferredLabels = score === 2 ? ['恰当', '通过'] : score === 1 ? ['轻微', '萌芽'] : ['严重', '不通过'];
    } else if (row['一级分类'] === '照顾者报告') {
      if (domain === '儿童现时发展程度') {
        score = ['沟通', '社交', '整体'].some((k) => row['评估项目'].includes(k)) ? 1 : 2;
      } else if (domain === '诊断类别及程度') {
        if (row['评估项目'].includes('自闭症-诊断类别')) score = 2;
        else if (row['评估项目'].includes('语言障碍-诊断类别')) score = 2;
        else if (row['评估项目'].includes('影响程度')) score = row['评估项目'].includes('自闭症') ? 1 : 2;
        else score = 0;
      } else if (domain === '问题行为-PB') {
        score = chooseFromPattern(withinDomain, { 2: 2, 1: 5, 0: 3 }, [2, 1, 0]);
      } else if (domain === '个人自理-PSC') {
        score = chooseFromPattern(withinDomain, { 2: 7, 1: 4, 0: 2 }, [2, 1, 0]);
      } else if (domain === '适应行为-AB') {
        score = chooseFromPattern(withinDomain, { 2: 6, 1: 6, 0: 3 }, [2, 1, 0]);
      }
      preferredLabels = score === 2 ? ['是', '轻微', '没有出现', '3-4岁', '通过'] : score === 1 ? ['中度', '轻微/中度', '2-3岁', '萌芽'] : ['严重', '不是', '<2岁', '不通过'];
    }

    const options = buildOptions(row);
    const selectedOption = optionKeyForScore(options, score, preferredLabels);
    const selected = options[selectedOption] || { value: String(score), label: '', description: '' };

    return {
      sort: Number(row['排序']) || idx + 1,
      category1: row['一级分类'],
      category2: domain,
      itemName: row['评估项目'],
      description: row['操作描述'],
      materials: row['所需材料'],
      score,
      selectedOption,
      selectedScore: Number(selected.value),
      selectedLabel: selected.label,
      note: idx % 29 === 0 ? notes[(idx / 29) % notes.length | 0] : '',
      options,
    };
  });

  const development = summarizeByDomain(
    answers,
    (answer) => answer.category1 === '发展副测验',
    ['通过', '萌芽', '不通过'],
  );
  const behavior = summarizeByDomain(
    answers,
    (answer) => answer.category1 === '行为副测验',
    ['恰当', '轻微', '严重', '通过', '萌芽', '不通过'],
  );

  return {
    childInfo: {
      name: '林小宇',
      gender: '男',
      birthDate: '2021-07-12',
      assessmentDate: '2026-04-18',
      assessmentEndDate: '2026-04-20',
      ageAtAssessment: '4岁9个月',
      diagnosisAge: '3岁6个月',
      diagnosisResult: '孤独症谱系障碍',
      diagnosisHospital: '市儿童医院发育行为科',
      family: '父母及外祖母共同照看',
      educationHistory: '曾接受半年机构一对一训练，近期每周3次语言与认知课程',
      isFirstAssessment: false,
    },
    summary: {
      profile: '精细动作、粗大动作和视觉动作模仿相对较好，语言表达、语言理解和社交互动为主要薄弱领域',
      developmentDomains: development,
      behaviorDomains: behavior,
      developmentTotal: answers.filter((a) => a.category1 === '发展副测验').reduce((sum, a) => sum + a.score, 0),
      behaviorTotal: answers.filter((a) => a.category1 === '行为副测验').reduce((sum, a) => sum + a.score, 0),
      caregiverSummary: '照顾者报告提示沟通、社交和问题行为仍需持续支持，自理能力部分具备基础。',
    },
    observations: {
      assessmentBehavior: '儿童能在熟悉材料出现时较快进入任务，语言类任务中等待时间较短。',
      cooperation: '精细操作和拼图类任务配合较好，转换到口语问答时需要重复提示。',
      attention: '单项任务注意约1-3分钟，视觉提示和实物强化可延长参与时间。',
      communication: '以手势、拿取和少量单词表达需要，主动口语表达不足。',
      socialResponse: '能接受成人短暂互动，但眼神接触和主动回应不稳定。',
      sensoryResponse: '对部分声音和触觉材料反应偏敏感，强度不高但会影响任务持续。',
      caregiverNotes: '家长反映在家中可完成部分生活自理步骤，但需要成人提醒和等待。',
    },
    answers,
  };
}

function makeCpepCase() {
  const rows = readCsv('data/cpep-config-v3.csv');
  const domainIndex = {};
  const developmentTargets = {
    '模仿': { 2: 4, 1: 4, 0: 2 },
    '知觉': { 2: 7, 1: 3, 0: 1 },
    '精细动作': { 2: 8, 1: 2, 0: 0 },
    '粗大动作': { 2: 7, 1: 3, 0: 1 },
    '手眼协调': { 2: 8, 1: 4, 0: 2 },
    '认知表现': { 2: 8, 1: 6, 0: 6 },
    '口语认知': { 2: 4, 1: 5, 0: 10 },
  };
  const pathologyTargets = {
    '情感': { 2: 3, 1: 2, 0: 1 },
    '人际关系': { 2: 2, 1: 3, 0: 2 },
    '物品喜好': { 2: 3, 1: 2, 0: 1 },
    '感觉模式': { 2: 6, 1: 5, 0: 3 },
    '语言': { 2: 3, 1: 4, 0: 4 },
  };
  const supplementTargets = {
    '模仿': { 1: 1, 0: 1 },
    '知觉': { 1: 1, 0: 1 },
    '精细动作': { 1: 2, 0: 1 },
    '粗大动作': { 1: 3, 0: 1 },
    '手眼协调': { 1: 2, 0: 1 },
    '认知表现': { 1: 4, 0: 8 },
    '口语认知': { 1: 1, 0: 5 },
  };
  const notes = [
    '示范后愿意尝试，但独立完成不稳定',
    '对视觉材料兴趣较高，可作为教学切入点',
    '口语回答常需要选择项或首音提示',
    '遇到转换任务时会短暂离座',
    '精细动作任务中持续性较好',
    '对响铃和触觉材料有轻微回避',
  ];

  const answers = rows.map((row, idx) => {
    const domain = row['二级分类'];
    const key = `${row['一级分类']}::${domain}`;
    domainIndex[key] = domainIndex[key] || 0;
    const withinDomain = domainIndex[key];
    domainIndex[key] += 1;

    let score = 2;
    let preferredLabels = ['P', 'A', 'H'];
    if (row['一级分类'] === '发展') {
      score = chooseFromPattern(withinDomain, developmentTargets[domain], [2, 1, 0]);
      preferredLabels = score === 2 ? ['P'] : score === 1 ? ['E'] : ['F'];
    } else if (row['一级分类'] === '病理学') {
      score = chooseFromPattern(withinDomain, pathologyTargets[domain], [2, 1, 0]);
      preferredLabels = score === 2 ? ['A'] : score === 1 ? ['M'] : ['S'];
    } else if (row['一级分类'] === '补充项目') {
      score = chooseFromPattern(withinDomain, supplementTargets[domain], [1, 0]);
      preferredLabels = score === 1 ? ['H'] : ['L'];
    }

    const options = buildOptions(row);
    const selectedOption = optionKeyForScore(options, score, preferredLabels);
    const selected = options[selectedOption] || { value: String(score), label: '', description: '' };

    return {
      sort: Number(row['排序']) || idx + 1,
      category1: row['一级分类'],
      category2: domain,
      itemName: row['评估项目'],
      description: row['操作描述'],
      materials: row['所需材料'],
      score,
      selectedOption,
      selectedScore: Number(selected.value),
      selectedLabel: selected.label,
      note: idx % 23 === 0 ? notes[(idx / 23) % notes.length | 0] : '',
      options,
    };
  });

  const development = summarizeByDomain(
    answers,
    (answer) => answer.category1 === '发展',
    ['P', 'E', 'F'],
  );
  const pathology = summarizeByDomain(
    answers,
    (answer) => answer.category1 === '病理学',
    ['A', 'M', 'S'],
  );
  const supplementary = summarizeByDomain(
    answers,
    (answer) => answer.category1 === '补充项目',
    ['H（通过）', 'L（不通过）'],
  );

  return {
    childInfo: {
      name: '陈小禾',
      gender: '女',
      birthDate: '2021-11-03',
      assessmentDate: '2026-04-22',
      assessmentEndDate: '2026-04-23',
      ageAtAssessment: '4岁5个月',
      diagnosisAge: '3岁2个月',
      diagnosisResult: 'ASD倾向，语言发育迟缓',
      diagnosisHospital: '妇幼保健院儿童保健科',
      family: '父母共同照看，白天由母亲陪伴训练',
      educationHistory: '已接受3个月机构早期干预，以认知、语言和感觉统合课程为主',
      isFirstAssessment: false,
    },
    summary: {
      profile: '精细动作、知觉和手眼协调为相对优势，口语认知、认知表现和人际互动为重点干预方向',
      developmentDomains: development,
      pathologyDomains: pathology,
      supplementaryDomains: supplementary,
      developmentPCount: answers.filter((a) => a.category1 === '发展' && a.selectedLabel === 'P').length,
      developmentECount: answers.filter((a) => a.category1 === '发展' && a.selectedLabel === 'E').length,
      developmentFCount: answers.filter((a) => a.category1 === '发展' && a.selectedLabel === 'F').length,
      pathologySCount: answers.filter((a) => a.category1 === '病理学' && a.selectedLabel === 'S').length,
      supplementaryPassCount: answers.filter((a) => a.category1 === '补充项目' && a.selectedLabel === 'H（通过）').length,
    },
    observations: {
      assessmentBehavior: '儿童进入评估后能接受熟悉材料，遇到口语问答和社交互动任务时参与度下降。',
      cooperation: '桌面操作任务配合较好，口语模仿和回答问题需要较多等待和提示。',
      attention: '对图片、拼图和泡泡材料注意较稳定，对声音刺激和新材料有短暂回避。',
      communication: '能用单词或手势表达部分需求，但主动表达少，回答问题依赖提示。',
      socialResponse: '能接受成人靠近和简单轮流，但主动互动和眼神协调不稳定。',
      playInterest: '偏好操作性材料，象征性游戏和与人共同游戏较少。',
      sensoryResponse: '对触觉块和响铃有轻微敏感表现，经过示范后可继续参与。',
      caregiverNotes: '家长希望优先提升主动表达、听指令和与同伴互动能力。',
    },
    answers,
  };
}

const outputs = [
  ['data/pep3-test-case-1.json', makePep3Case()],
  ['data/cpep-test-case-1.json', makeCpepCase()],
];

outputs.forEach(([relPath, data]) => {
  fs.writeFileSync(path.join(ROOT, relPath), `${JSON.stringify(data, null, 2)}\n`);
  console.log(`${relPath}: ${data.answers.length} answers`);
});
