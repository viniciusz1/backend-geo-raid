from flask import jsonify, request
from app import db
from app.models import Character, Usuario, Quest
from app.routes import bp
from app.auth import token_required


@bp.route("/quests", methods=["POST"])
@token_required
def create_quest(current_user):
    data = request.get_json()
    if not data or not data.get('questao') or not data.get('dificuldade'):
        return jsonify({"error": "Dados insuficientes: 'questao' e 'dificuldade' são obrigatórios"}), 400

    # Validação opcional da dificuldade
    allowed_difficulties = ["easy", "medium", "hard", "facil", "medio", "dificil"]
    if data.get('dificuldade').lower() not in allowed_difficulties:
        return jsonify({"error": f"Dificuldade inválida. Permitidas: {', '.join(allowed_difficulties)}"}), 400
    
    # Verificar se a questão já existe
    if Quest.query.filter_by(questao=data['questao']).first():
        return jsonify({"error": "Questão já existe"}), 409

    try:
        new_quest = Quest(
            questao=data['questao'],
            dificuldade=data['dificuldade'].lower()
        )
        db.session.add(new_quest)
        db.session.commit()
        return jsonify(new_quest.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao criar questão", "details": str(e)}), 500
    
@bp.route("/quests", methods=["GET"])
@token_required
def get_all_quests(current_user):
    dificuldade_filter = request.args.get('dificuldade')
    try:
        query = Quest.query
        if dificuldade_filter:
            query = query.filter(Quest.dificuldade.ilike(dificuldade_filter))
        
        quests = query.all()
        return jsonify([quest.to_dict() for quest in quests]), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar questões", "details": str(e)}), 500
    
@bp.route("/quests/<int:quest_id>", methods=["GET"])
@token_required
def get_quest_by_id(current_user, quest_id):
    try:
        quest = Quest.query.get_or_404(quest_id)
        return jsonify(quest.to_dict()), 200
    except Exception as e:
        if hasattr(e, 'code') and e.code == 404:
             return jsonify({"error": "Questão não encontrada"}), 404
        return jsonify({"error": "Erro ao buscar questão", "details": str(e)}), 500
    
@bp.route("/quests/<int:quest_id>", methods=["PUT"])
@token_required
def update_quest(current_user, quest_id):
    try:
        quest = Quest.query.get_or_404(quest_id)
    except Exception as e:
         if hasattr(e, 'code') and e.code == 404:
             return jsonify({"error": "Questão não encontrada para atualizar"}), 404
         return jsonify({"error": "Erro ao buscar questão para atualizar", "details": str(e)}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado fornecido para atualização"}), 400

    updated = False
    if 'questao' in data:
        # Opcional: verificar se a nova questão já existe (pertencente a outra quest)
        existing_quest = Quest.query.filter(Quest.questao == data['questao'], Quest.id != quest_id).first()
        if existing_quest:
            return jsonify({"error": "Outra questão com este texto já existe"}), 409
        quest.questao = data['questao']
        updated = True
        
    if 'dificuldade' in data:
        allowed_difficulties = ["easy", "medium", "hard", "facil", "medio", "dificil"]
        if data['dificuldade'].lower() not in allowed_difficulties:
            return jsonify({"error": f"Dificuldade inválida. Permitidas: {', '.join(allowed_difficulties)}"}), 400
        quest.dificuldade = data['dificuldade'].lower()
        updated = True

    if not updated:
        return jsonify({"message": "Nenhum campo válido fornecido para atualização"}), 400

    try:
        db.session.commit()
        return jsonify(quest.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar questão", "details": str(e)}), 500

@bp.route("/quests/<int:quest_id>", methods=["DELETE"])
@token_required
def delete_quest(current_user, quest_id):
    try:
        quest = Quest.query.get_or_404(quest_id)
    except Exception as e:
         if hasattr(e, 'code') and e.code == 404:
             return jsonify({"error": "Questão não encontrada para deletar"}), 404
         return jsonify({"error": "Erro ao buscar questão para deletar", "details": str(e)}), 500
    
    try:
        db.session.delete(quest)
        db.session.commit()
        return jsonify({"message": "Questão deletada com sucesso"}), 200 # Ou 204 No Content com corpo vazio
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar questão", "details": str(e)}), 500
    
@bp.route("/populate-quests", methods=["POST"])
@token_required # Proteger esta rota, talvez com um papel de admin no futuro
def populate_initial_quests(current_user):
    # Verifique se já existem questões para evitar duplicação
    if Quest.query.count() > 0:
        # Você pode optar por deletar todas e recriar, ou apenas adicionar se estiverem faltando.
        # Por simplicidade, vamos apenas retornar uma mensagem se já houver questões.
        # Para uma lógica mais robusta, você verificaria cada questão individualmente.
        return jsonify({"message": "Banco de dados de questões já parece populado."}), 409 # Conflict

    initial_quests_data = [
        # 5 Questões Fáceis
        {"questao": "Qual é a cor do céu em um dia claro?", "dificuldade": "easy"},
        {"questao": "Quantos dias tem uma semana?", "dificuldade": "easy"},
        {"questao": "Qual animal mia e tem bigodes?", "dificuldade": "easy"},
        {"questao": "O que usamos para escrever em um caderno?", "dificuldade": "easy"},
        {"questao": "Qual é o oposto de 'quente'?", "dificuldade": "easy"},
        # 5 Questões Médias
        {"questao": "Quem descobriu o Brasil?", "dificuldade": "medium"},
        {"questao": "Quantos planetas existem no sistema solar (incluindo Plutão como anão)?", "dificuldade": "medium"},
        {"questao": "Qual é a capital da França?", "dificuldade": "medium"},
        {"questao": "Em que ano começou a Segunda Guerra Mundial?", "dificuldade": "medium"},
        {"questao": "Qual elemento químico tem o símbolo 'O'?", "dificuldade": "medium"},
        # 5 Questões Difíceis
        {"questao": "Qual é a velocidade da luz no vácuo (aproximadamente)?", "dificuldade": "hard"},
        {"questao": "Quem escreveu 'Dom Quixote'?", "dificuldade": "hard"},
        {"questao": "Qual é o teorema fundamental da aritmética?", "dificuldade": "hard"},
        {"questao": "Qual o nome do processo pelo qual as plantas produzem seu alimento?", "dificuldade": "hard"},
        {"questao": "Quem foi o primeiro programador de computadores reconhecido historicamente?", "dificuldade": "hard"}
    ]

    try:
        for q_data in initial_quests_data:
            # Pequena verificação para evitar duplicatas se rodar múltiplas vezes e a primeira verificação falhar
            if not Quest.query.filter_by(questao=q_data["questao"]).first():
                quest = Quest(questao=q_data["questao"], dificuldade=q_data["dificuldade"])
                db.session.add(quest)
        db.session.commit()
        return jsonify({"message": f"{len(initial_quests_data)} questões iniciais adicionadas com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao popular questões iniciais", "details": str(e)}), 500