-- CreateTable
CREATE TABLE "User" (
    "userId" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Chat" (
    "chatId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_Id" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Message" (
    "messageId" TEXT NOT NULL,
    "chat_Id" TEXT,
    "content" TEXT NOT NULL,
    "profileImgUrl" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "User_userId_key" ON "User"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "Chat_chatId_key" ON "Chat"("chatId");

-- CreateIndex
CREATE UNIQUE INDEX "Message_messageId_key" ON "Message"("messageId");

-- AddForeignKey
ALTER TABLE "Chat" ADD CONSTRAINT "Chat_user_Id_fkey" FOREIGN KEY ("user_Id") REFERENCES "User"("userId") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Message" ADD CONSTRAINT "Message_chat_Id_fkey" FOREIGN KEY ("chat_Id") REFERENCES "Chat"("chatId") ON DELETE SET NULL ON UPDATE CASCADE;
