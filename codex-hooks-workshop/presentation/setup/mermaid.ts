import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  fontFamily: 'Arial, sans-serif',
  themeVariables: {
    fontSize: '19px',
    primaryColor: '#18364a',
    primaryTextColor: '#e8edf5',
    primaryBorderColor: '#6ee7c0',
    lineColor: '#6ee7c0',
    secondaryColor: '#152638',
    tertiaryColor: '#101c2c',
    edgeLabelBackground: '#101c2c',
  },
  flowchart: {
    htmlLabels: false,
    curve: 'linear',
    padding: 12,
    nodeSpacing: 25,
    rankSpacing: 30,
  },
}))
