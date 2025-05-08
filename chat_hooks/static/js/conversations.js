// Função para redirecionar para a página de conversa
function formatarData(data) {
  const partes = data.split("T");
  const dataFormatada = partes[0].split("-").reverse().join("/");
  if (partes[1]) {
    return `${dataFormatada} ${partes[1].substring(0, 5)}`;
  } else {
    return dataFormatada;
  }
}

async function carregarMensagens(conversation_id) {
  const main = document.querySelector("main");
  main.innerHTML = "";
  try {
    const response = await fetch(`/conversations/${conversation_id}/`);
    if (!response.ok) {
      throw new Error(`Status ${response.status}`);
    }
    const data_conversation = await response.json();

    // Cria e insere o cabeçalho com os dados da conversa
    const headerDiv = createHeaderDiv(data_conversation);
    main.insertBefore(headerDiv, main.firstChild);

    // Criando o container para as mensagens
    const containerMessages = document.createElement("div");
    containerMessages.classList.add(
      "flex",
      "flex-col",
      "gap-4",
      "mt-4",
      "flex-1",
      "overflow-y-auto"
    );
    main.appendChild(containerMessages);

    // Cria e adiciona cada bloco de mensagem
    data_conversation.messages.forEach((message) => {
      const messageBlock = createMessageBlock(message);
      containerMessages.appendChild(messageBlock);
    });

    // Ajusta o scroll para o final
    containerMessages.scrollTop = containerMessages.scrollHeight;
  } catch (error) {
    console.error("Erro ao buscar mensagens:", error);
    showError(main, error.message || "Erro ao carregar mensagens");
  }
}

function createHeaderDiv(data) {
  const headerDiv = document.createElement("div");
  headerDiv.classList.add(
    "w-full",
    "p-4",
    "text-white",
    "rounded",
    "shadow-md",
    "mb-4"
  );

  // Define a cor de fundo conforme o status da conversa
  if (data.status === "CLOSED") {
    headerDiv.classList.add("bg-red-500");
  } else {
    headerDiv.classList.add("bg-blue-500");
  }

  const conversationStatus = document.createElement("p");
  conversationStatus.innerText = `Status da conversa: ${data.status}`;
  headerDiv.appendChild(conversationStatus);

  const conversationCreatedAt = document.createElement("p");
  conversationCreatedAt.innerText = `Criada em: ${formatarData(
    data.created_at
  )}`;
  headerDiv.appendChild(conversationCreatedAt);

  if (data.status === "CLOSED") {
    const conversationClosedAt = document.createElement("p");
    conversationClosedAt.innerText = `Fechada em: ${formatarData(
      data.updated_at
    )}`;
    headerDiv.appendChild(conversationClosedAt);
  }

  return headerDiv;
}

function createMessageBlock(message) {
  const messageBlock = document.createElement("div");
  messageBlock.classList.add(
    "max-w-md",
    "rounded-lg",
    "px-4",
    "py-2",
    "my-2",
    "shadow-md",
    "text-white"
  );

  // Aplica cores e alinhamento conforme a direção da mensagem
  if (message.direction === "SENT") {
    messageBlock.classList.add("bg-blue-500", "ml-0", "mr-auto");
  } else {
    messageBlock.classList.add("bg-green-500", "ml-auto", "mr-2");
  }

  // Cabeçalho com id
  const header = document.createElement("div");
  header.classList.add("flex", "justify-between", "text-sm", "mb-1");

  const messageId = document.createElement("span");
  messageId.innerText = `ID: ${message.id}`;
  header.appendChild(messageId);

  // Conteúdo da mensagem
  const content = document.createElement("p");
  content.innerText = message.content;
  content.classList.add("text-base", "mt-1");

  // Rodapé com a direção e data/hora
  const footerDiv = document.createElement("div");
  footerDiv.classList.add("flex", "justify-between", "items-center", "mt-1");

  const directionTag = document.createElement("p");
  directionTag.innerText = `Direction: ${message.direction}`;
  directionTag.classList.add("text-xs", "text-gray-200");

  const timeSpan = document.createElement("span");
  timeSpan.innerText = formatarData(message.created_at);
  timeSpan.classList.add("text-xs", "text-gray-200");

  footerDiv.appendChild(directionTag);
  footerDiv.appendChild(timeSpan);

  messageBlock.appendChild(header);
  messageBlock.appendChild(content);
  messageBlock.appendChild(footerDiv);

  return messageBlock;
}

function showError(container, errorMessage) {
  container.innerHTML = "";
  const errorDiv = document.createElement("div");
  errorDiv.classList.add(
    "w-full",
    "p-4",
    "bg-red-500",
    "text-white",
    "rounded",
    "shadow-md",
    "mb-4",
    "text-center"
  );
  errorDiv.innerText = `Erro: ${errorMessage}`;
  container.appendChild(errorDiv);
}

async function carregarConversas() {
  const conversationButtons = document.getElementById("conversation-buttons");
  conversationButtons.innerHTML = "";
  try {
    const conversations = await fetchConversations();
    const container = createConversationButtonsContainer(conversations);
    conversationButtons.appendChild(container);
  } catch (error) {
    console.error("Erro ao buscar conversas:", error);
    showError(conversationButtons, error.message || "Erro ao buscar conversas");
  }
}

async function fetchConversations() {
  const response = await fetch("/conversations/");
  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }
  return response.json();
}

function createConversationButtonsContainer(conversations) {
  const container = document.createElement("div");
  container.classList.add("flex", "flex-col", "items-center", "gap-4", "mt-4");

  conversations.forEach((conversation) => {
    const button = createConversationButton(conversation);
    container.appendChild(button);
  });

  return container;
}

function createConversationButton(conversation) {
  const button = document.createElement("button");
  button.innerHTML = `Conversa: ${conversation.id} <br> Status: ${conversation.status}`;

  if (conversation.status === "CLOSED") {
    button.classList.add(
      "w-full",
      "bg-gradient-to-r",
      "from-red-500",
      "to-red-700",
      "text-white",
      "py-2",
      "rounded-md",
      "shadow-lg",
      "hover:from-red-600",
      "hover:to-red-800",
      "transition",
      "duration-300",
      "ease-in-out",
      "transform",
      "hover:scale-105"
    );
  } else {
    button.classList.add(
      "w-full",
      "bg-gradient-to-r",
      "from-blue-500",
      "to-blue-700",
      "text-white",
      "py-2",
      "rounded-md",
      "shadow-lg",
      "hover:from-blue-600",
      "hover:to-blue-800",
      "transition",
      "duration-300",
      "ease-in-out",
      "transform",
      "hover:scale-105"
    );
  }

  button.onclick = () => carregarMensagens(conversation.id);
  return button;
}
carregarConversas();
