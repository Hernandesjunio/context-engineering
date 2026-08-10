local callout_types = {
  warning = "warningbox",
  tip = "tipbox",
  info = "infobox",
  evidence = "evidencebox",
  example = "examplebox",
  curious = "curiousbox",
}

local default_titles = {
  warning = "Atenção",
  tip = "Dica rápida",
  info = "Contexto",
  evidence = "Evidência",
  example = "Exemplo",
  curious = "Para curiosos",
}

local function escape_latex(value)
  return value
    :gsub("\\", "\\textbackslash{}")
    :gsub("([%%$#&_{}])", "\\%1")
end

function Div(element)
  for callout_type, environment in pairs(callout_types) do
    if element.classes:includes(callout_type) then
      local title = element.attributes.title or default_titles[callout_type]
      local open = pandoc.RawBlock(
        "latex",
        string.format("\\begin{%s}{%s}", environment, escape_latex(title))
      )
      local close = pandoc.RawBlock("latex", string.format("\\end{%s}", environment))
      local blocks = { open }
      for _, block in ipairs(element.content) do
        table.insert(blocks, block)
      end
      table.insert(blocks, close)
      return blocks
    end
  end
end
