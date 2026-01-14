import { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle, HeadingLevel, AlignmentType } from "docx";
import { saveAs } from "file-saver";
import { DidacticSequence, SequenceInput } from "../types";

export const generateDocx = async (data: DidacticSequence, input: SequenceInput) => {
  const tableHeaderStyle = {
    fill: { type: "pattern", pattern: "solid", fgColor: "E5E7EB" },
    margins: { top: 100, bottom: 100, left: 100, right: 100 },
  };



  const createRow = (label: string, value: string) => {
    return new TableRow({
      children: [
        new TableCell({
          width: { size: 30, type: WidthType.PERCENTAGE },
          // shading removed
          children: [new Paragraph({ children: [new TextRun({ text: label, bold: true })] })],
        }),
        new TableCell({
          width: { size: 70, type: WidthType.PERCENTAGE },
          children: [new Paragraph({ children: [new TextRun(value || "")] })],
        }),
      ],
    });
  };

  const activitiesRows = data.actividades.flatMap((act) => [
    new TableRow({
      children: [
        new TableCell({
          columnSpan: 2,
          // shading removed
          children: [
            new Paragraph({
              children: [new TextRun({ text: `Sesión ${act.sesion} (${act.tiempo})`, bold: true })],
              alignment: AlignmentType.CENTER,
            }),
          ],
        }),
      ],
    }),
    createRow("Descripción", act.descripcion),
    createRow("Materiales", act.materiales.join(", ")),
    createRow("Imprimibles", act.imprimibles),
  ]);

  const rubricRows = [
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Criterio", bold: true })] })] }),
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Básico", bold: true })] })] }),
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Satisfactorio", bold: true })] })] }),
        new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "Avanzado", bold: true })] })] }),
      ]
    }),
    ...data.rubrica.map(r => new TableRow({
      children: [
        new TableCell({ children: [new Paragraph(r.criterio)] }),
        new TableCell({ children: [new Paragraph(r.basico)] }),
        new TableCell({ children: [new Paragraph(r.satisfactorio)] }),
        new TableCell({ children: [new Paragraph(r.avanzado)] }),
      ]
    }))
  ];

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          new Paragraph({
            text: "INSTITUCIÓN EDUCATIVA GUAIMARAL",
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER,
          }),
          new Paragraph({
            text: "FORMATO DE SECUENCIA DIDÁCTICA",
            heading: HeadingLevel.HEADING_2,
            alignment: AlignmentType.CENTER,
          }),
          new Paragraph({ text: "" }), // Spacer

          // General Info Table
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: [
              createRow("Grado", input.grado),
              createRow("Área", input.area),
              createRow("Tema", input.tema),
              createRow("DBA", data.dba_utilizado || input.dba),
              createRow("Eje CRESE", input.ejeCrese),
              createRow("Objetivo de Aprendizaje", data.objetivo_aprendizaje),
              createRow("Estándar", data.estandar),
              createRow("Competencias MEN", data.competencias_men),
              createRow("Metodología", data.metodologia),
              createRow("Corporiedad (ADI)", data.corporiedad_adi),
              createRow("Productos Asociados", data.productos_asociados),
              createRow("Instrumentos de Evaluación", data.instrumentos_evaluacion),
              createRow("Adecuaciones PIAR", data.adecuaciones_piar),
              createRow("Bibliografía", data.bibliografia),
              createRow("Observaciones", data.observaciones),
            ],
          }),

          new Paragraph({ text: "" }),
          new Paragraph({ text: "ACTIVIDADES DETALLADAS", heading: HeadingLevel.HEADING_3 }),
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: activitiesRows,
          }),

          new Paragraph({ text: "" }),
          new Paragraph({ text: "RÚBRICA DE EVALUACIÓN", heading: HeadingLevel.HEADING_3 }),
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: rubricRows
          }),

          new Paragraph({ text: "" }),
          new Paragraph({ text: "TALLER / EVALUACIÓN", heading: HeadingLevel.HEADING_3 }),
          ...data.evaluacion.map((item, i) => new Paragraph({
            text: `${i + 1}. ${item.pregunta}`,
            spacing: { after: 200 }
          })),

          new Paragraph({ text: "" }),
          new Paragraph({ text: "RECURSOS", heading: HeadingLevel.HEADING_3 }),
          ...data.recursos.map(r => new Paragraph({
            children: [
              new TextRun({ text: `• ${r.nombre}: `, bold: true }),
              new TextRun(r.descripcion)
            ]
          }))
        ],
      },
    ],
  });

  const blob = await Packer.toBlob(doc);
  saveAs(blob, `Secuencia_${input.area}_${input.grado}.docx`);
};
