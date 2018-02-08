$(document).ready(function () {
    function init_select2() {
        $.fn.select2.defaults.set('language', 'pt-BR');
        $.fn.select2.defaults.set('allowClear', true);
        $.fn.select2.defaults.set('placeholder', '');
        $.fn.select2.defaults.set('width', '100%');

        $('#id_municipio.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/municipios/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        estado__sigla: $('#id_esatdo').val() !== null ? $('#id_estado').val() : 0
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: $.map(data.results, function (val, i) {
                            val['id'] = val['ibge'];
                            return val;
                        }),
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (municipio) {
                if (municipio !== undefined)
                    return municipio.nome;
                else
                    return undefined;
            },
            initSelection: function(element, callback) {
                if (element.val() === '' && element.val()) return;
                return $.getJSON("/api/v1/comum/municipios/pesquisar/?ibge=" + (element.val() !== null ? element.val(): 0), null, function(data) {
                    if (data.results.length > 0)
                        return callback($.map(data.results, function (val, i) {
                            val['id'] = val['ibge'];
                            return val;
                        })[0]);
                });
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (municipio) {
                if (municipio === undefined || municipio.id === undefined) return '<div>Pesquisando...</div>';

                return municipio.nome;
            },

            cache: true
        });

        $('#id_equipe_saude.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/equipes-saude/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        unidade__id: $('#id_unidade_saude').val() !== null ? $('#id_unidade_saude').val() : 0
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (equipe) {
                if (equipe !== undefined)
                    return equipe.nome;
                else
                    return undefined;
            },
            // initSelection: function(element, callback) {
            //     if (element.val() === '') return;
            //     return $.getJSON("/api/v1/comum/equipes-saude/pesquisar/?id=" + (element.val() !== null ? element.val(): 0), null, function(data) {
            //         if (data.results.length > 0)
            //             return callback(data.results[0]);
            //     });
            // },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (equipe) {
                if (equipe === undefined || equipe.id === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + (equipe.nome !== undefined ? equipe.nome : '---') + '</p>' +
                    '<p><strong>INE: </strong>' + (equipe.ine !== undefined ? equipe.ine : '---') + '</p></div></div>';
            }
        });

        $('#id_unidade[multiple]').select2({
            ajax: {
                url: '/api/v1/comum/unidades-saude/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (unidade) {
                if (unidade !== undefined)
                    return unidade.nome !== undefined ? unidade.nome : unidade.text;
                else
                    return undefined;
            },
            initSelection: function (element, callback) {
                var valores = $(element).val();
                var query = '';

                if (! $.isArray(valores)){
                    query = '?id__in[]=' + (valores !== null ? valores: 0)
                } else{
                    $.each(valores, function (i, el) {
                       query += (i !== 0 ? '&': '') + 'id__in[]=' + (el !== null ? el: 0)
                    });
                }

                if (query === '') {
                    callback([]);
                    return;
                }

                $.getJSON("/api/v1/comum/unidades-saude/pesquisar/?" + query, null, function(data) {
                    callback(data.results);
                });
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (unidade) {
                if (unidade === undefined || unidade.id === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + (unidade.nome !== undefined ? unidade.nome : '---') + '</p>' +
                    '<p><strong>CNES: </strong>' + (unidade.cnes !== undefined ? unidade.cnes : '---') + '</p></div></div>';
            },
            cache: true,
            minimumInputLength: 3,
            minimumSelectionLength: 1
        });

        $('#id_responsavel.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/profissionais-gema/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        'matriciadora|referencia|equipegema': $('#id_equipe_gema').val(),
                        'profissionais_base__profissao': $('#id_funcao').val()
                        // profissionalgema__isnull: true
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                }
            },
            initSelection: function(element, callback) {
                if (element.val() === null || element.val() === "") return;
                $.getJSON("/api/v1/comum/profissionais-gema/pesquisar/?id=" + (element.val() !== null ? element.val(): 0), null, function(data) {
                    callback(data.results[0]);
                });
            },
            templateSelection: function (profissional) {
                if (profissional !== undefined) {
                    return profissional.username;
                }
                return undefined;
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (profissional) {
                if (profissional === undefined || profissional.id === undefined) return '<div>Pesquisando...</div>';

                return profissional.username;
            }
        });

        $('#id_equipe_gema').change(function () {
            $('#id_funcao').empty().trigger('change');
        });

        $('#id_funcao.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/profissoes/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        'profissional__profissionalgema__matriciadora|profissional__profissionalgema__referencia|profissional__profissionalgema__equipegema': $('#id_equipe_gema').val()
                        // profissionalgema__isnull: true
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: $.map(data.results, function (el, i) {el['id'] = el['cbo']; return el;}),
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            initSelection: function(element, callback) {
                if (element.val() === null || element.val() === "") return;
                $.getJSON("/api/v1/comum/profissoes/pesquisar/?cbo=" + (element.val() !== null ? element.val(): 0), null, function(data) {
                    callback($.map(data.results, function (el, i) {el['id'] = el['cbo']; return el;})[0]);
                });
            },
            templateSelection: function (profissao) {
                $('#id_responsavel').empty().trigger('change');
                if (profissao !== undefined) {
                    return (profissao.descricao !== undefined ? profissao.descricao : profissao.text);
                }
                return undefined;
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (profissao) {
                if (profissao === undefined || profissao.cbo === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + profissao.descricao + '</p>' +
                    '<p><strong>CBO: </strong>' + profissao.cbo + '</p></div>';
            },
        });

        $('#id_filtro_funcao.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/profissoes/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        profissional__profissionalgema__isnull: false
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: $.map(data.results, function (el, i) {el['id'] = el['cbo']; return el;}),
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (profissao) {
                if (profissao !== undefined) {
                    return (profissao.descricao !== undefined ? profissao.descricao : profissao.text);
                }
                return undefined;
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (profissao) {
                if (profissao === undefined || profissao.cbo === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + profissao.descricao + '</p>' +
                    '<p><strong>CBO: </strong>' + profissao.cbo + '</p></div>';
            },
        });

        $('#id_equipes_add.pesquisa').select2({
            ajax: {
                url: '/api/v1/main/equipes-gema/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    if ($('#id_filtro_funcao').val() != null) {
                        return {
                            q: params.term, // search term
                            page: params.page,
                            'equipereferencia__profissionais__profissionais_base__profissao__cbo|equipematriciadora__profissionais__profissionais_base__profissao__cbo': $('#id_filtro_funcao').val()
                        };
                    } else {
                        return {
                            q: params.term, // search term
                            page: params.page
                        };
                    }

                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (equipe) {
                if (equipe !== undefined) {
                    return (equipe.nome);
                }
                return undefined;
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (equipe) {
                if (equipe === undefined || equipe.id === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + equipe.nome + '</p>';
            }
        });

        $('#id_profissionais_base.pesquisa').select2({
            ajax: {
                url: '/api/v1/comum/profissionais-equipe-saude/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page,
                        // profissionalgema__isnull: true
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            initSelection: function (element, callback) {
                var valores = $(element).val();
                var query = '';

                if (! $.isArray(valores)){
                    query = '?id__in[]=' + (valores !== null ? valores: 0)
                } else{
                    $.each(valores, function (i, el) {
                       query += (i !== 0 ? '&': '') + 'id__in[]=' + (el !== null ? el: 0)
                    });
                }

                if (query === '') {
                    callback([]);
                    return;
                }

                $.getJSON("/api/v1/comum/profissionais-equipe-saude/pesquisar/?" + query, null, function(data) {
                    callback(data.results);
                });
            },
            templateSelection: function (profissional) {
                if (profissional !== undefined) {
                    if (profissional.cpf !== null)
                        $("input[name=cpf]").val(profissional.cpf);
                        if (profissional.email !== null)
                            $("input[name=email]").val(profissional.email);
                    return profissional.nome !== undefined ? profissional.nome : profissional.text;
                }
                return undefined;
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (profissional) {
                if (profissional === undefined || profissional.id === undefined) return '<div>Pesquisando...</div>';
                return '<div class="select2-result clearfix"><div>' +
                    '<div class="col-md-6"><p><strong>Nome: </strong>' + (profissional.nome !== undefined ? profissional.nome : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>Funções: </strong>' + (profissional.profissoes !== undefined ? profissional.profissoes : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>CNS: </strong>' + (profissional.cns !== undefined ? profissional.cns : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>CPF: </strong>' + (profissional.cpf !== null ? profissional.cpf : '---') + '</p></div></div>' +
                    '<div class="col-md-6"><p><strong>Unidade de Saúde: </strong>' + (profissional.unidade !== null ? profissional.unidade : '---') + '</p></div></div></div>';
            },
            cache: true,
            minimumInputLength: 3
        });

        // $('#id_equipes.pesquisa').select2({
        //     ajax: {
        //         url: '/api/v1/main/equipes-gema/pesquisar/',
        //         dataType: 'json',
        //         delay: 250,
        //         data: function (params) {
        //             return {
        //                 q: params.term, // search term
        //                 page: params.page,
        //             };
        //         },
        //         processResults: function (data, params) {
        //             // parse the results into the format expected by Select2
        //             // since we are using custom formatting functions we do not need to
        //             // alter the remote JSON data, except to indicate that infinite
        //             // scrolling can be used
        //             params.page = params.page || 1;
        //
        //             return {
        //                 results: data.results,
        //                 pagination: {
        //                     more: (params.page * 20) < data.count
        //                 }
        //             };
        //         }
        //     },
        //     templateSelection: function (equipe) {
        //         if (equipe !== undefined)
        //             return equipe.nome;
        //         else
        //             return undefined;
        //     },
        //     escapeMarkup: function (markup) {
        //         if (markup) return markup; else return '';
        //     },
        //     initSelection: function (element, callback) {
        //         var valores = $(element).val();
        //         var query = '';
        //
        //         if (! $.isArray(valores)){
        //             query = 'id__in[]=' + (valores !== null ? valores: 0)
        //         } else{
        //             $.each(valores, function (i, el) {
        //                query += (i !== 0 ? '&': '') + 'id__in[]=' + (el !== null ? el: 0)
        //             });
        //         }
        //
        //         if (query === '') return;
        //
        //         $.getJSON("/api/v1/main/equipes-gema/pesquisar/?" + query, null, function(data) {
        //             callback(data.results);
        //         });
        //     },
        //     templateResult: function (equipe) {
        //         if (equipe === undefined || equipe.id === undefined) return '<div>Pesquisando...</div>';
        //
        //         return equipe.nome;
        //     },
        //     minimumInputLength: 3,
        //     minimumSelectionLength: 1
        // });

        $('#id_profissionais[multiple], #id_adm.pesquisa').each(function (i, el) {
            $(el).select2({
                ajax: {
                    url: '/api/v1/comum/profissionais-gema/pesquisar/',
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            q: params.term, // search term
                            page: params.page,
                            profissionais_base__profissionalequipesaude__unidade_saude__id__in: $('#id_unidade').prop('multiple') ? $('#id_unidade').val() : [$('#id_unidade').val()]
                        };
                    },
                    processResults: function (data, params) {
                        // parse the results into the format expected by Select2
                        // since we are using custom formatting functions we do not need to
                        // alter the remote JSON data, except to indicate that infinite
                        // scrolling can be used
                        params.page = params.page || 1;

                        return {
                            results: data.results,
                            pagination: {
                                more: (params.page * 20) < data.count
                            }
                        };
                    },
                },
                templateSelection: function (profissional) {
                    if (profissional !== undefined)
                        return profissional.username !== undefined ? profissional.username : profissional.text;
                    else
                        return undefined;
                },
                escapeMarkup: function (markup) {
                    if (markup) return markup; else return '';
                },
                initSelection: function (element, callback) {
                    var valores = $(element).val();
                    var query = '';

                    if (! $.isArray(valores)){
                        query = 'id__in[]=' + (valores !== null ? valores: 0)
                    } else{
                        $.each(valores, function (i, el) {
                           query += (i !== 0 ? '&': '') + 'id__in[]=' + (el !== null ? el: 0)
                        });
                    }

                    if (query === '') {
                        callback([]);
                        return;
                    }

                    $.getJSON("/api/v1/comum/profissionais-gema/pesquisar/?" + query, null, function(data) {
                        callback(data.results);
                    });
                },
                templateResult: function (profissional) {
                    if (profissional === undefined || profissional.id === undefined) return '<div>Pesquisando...</div>';
                    return '<div class="select2-result clearfix"><div>' +
                        '<div class="col-md-12"><p><strong>Nome: </strong>' + (profissional.username !== undefined ? profissional.username : '---') + '</p></div>' +
                        '<div class="col-md-6"><p><strong>CPF: </strong>' + (profissional.cpf !== undefined ? profissional.cpf : '---') + '</p></div>' +
                        '<div class="col-md-6"><p><strong>Funções: </strong>' + (profissional.profissoes.length > 0 ? profissional.profissoes : '---') + '</p></div></div></div>';
                },
                cache: true,
                minimumInputLength: 3,
                minimumSelectionLength: 1
            });
        });

        $('#id_unidade_saude.pesquisa, #id_unidade.pesquisa:not([multiple])').select2({
            ajax: {
                url: '/api/v1/comum/unidades-saude/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            templateSelection: function (unidade) {
                if (unidade !== undefined)
                    return unidade.nome;
                else
                    return undefined;
            },
            initSelection: function(element, callback) {
                if (element.val() === null) return;
                return $.getJSON("/api/v1/comum/unidades-saude/pesquisar/?id=" + (element.val() !== null ? element.val(): 0), null, function(data) {
                    return callback(data.results[0]);
                });
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (unidade) {
                if (unidade === undefined || unidade.id === undefined) return '<div>Pesquisando...</div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<p><strong>Nome: </strong>' + (unidade.nome !== undefined ? unidade.nome : '---') + '</p>' +
                    '<p><strong>CNES: </strong>' + (unidade.cnes !== undefined ? unidade.cnes : '---') + '</p></div></div>';
            },
            minimumInputLength: 3
        });

        var erro;

        $('#id_paciente_cpf.pesquisa').select2({
            ajax: {
                url: '/api/v1/main/pacientes/pesquisar/',
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function (data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;

                    return {
                        results: $.map(data.results, function (val, i) {
                            val['id'] = val['cpf'];
                            return val;
                        }),
                        pagination: {
                            more: (params.page * 20) < data.count
                        }
                    };
                },
            },
            initSelection: function(element, callback) {
                if (element.val() === null) return;

                $.getJSON("/api/v1/main/pacientes/pesquisar/?cpf=" + element.val(), null, function(data) {
                    paciente = $.map(data.results, function (val, i) {
                        val['id'] = val['cpf'];
                        return val;
                    })[0];
                    callback(paciente);
                });
            },
            tags: true,
            createTag: function (params) {
                return {
                    id: params.term,
                    text: params.term,
                    cpf: params.term,
                    newOption: true
                }
            },
            escapeMarkup: function (markup) {
                if (markup) return markup; else return '';
            },
            templateResult: function (paciente) {
                if (paciente.cpf === undefined) return;

                if (paciente.newOption) return '<div class="select2-result clearfix"><div>' +
                    '<div class="col-md-6"><p><strong>CPF: </strong>' + (paciente.cpf !== undefined ? paciente.cpf : '---') + '</p></div></div></div>';

                return '<div class="select2-result clearfix"><div>' +
                    '<div class="col-md-6"><p><strong>Nome: </strong>' + (paciente.nome !== undefined ? paciente.nome : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>CPF: </strong>' + (paciente.cpf !== undefined ? paciente.cpf : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>Número do SUS: </strong>' + (paciente.numero_sus !== undefined ? paciente.numero_sus : '---') + '</p></div>' +
                    '<div class="col-md-6"><p><strong>Data de nascimento: </strong>' + (paciente.data_nascimento !== undefined ? paciente.data_nascimento : '---') + '</p></div></div></div>';
            },
            templateSelection: function (paciente) {
                $('*[name="paciente_nome"]').val(paciente.nome);
                $('*[name="paciente_numero_sus"]').val(paciente.numero_sus);
                $('*[name="paciente_data_nascimento"]').val(paciente.data_nascimento);
                return paciente.cpf;
            },
            minimumInputLength: 3
        });

        $('.select2-input').select2();

        $('.select2-input-tags').select2({
            tags: true,
            tokenSeparators: [';', ',']
        });

    }

    function init_wysihtml5() {
        $('.wysihtml5').wysihtml5();
    }

    function init_datepicker() {
        $('.dateinput').datetimepicker({
            format: 'DD/MM/YYYY',
            locale: 'pt-br'
        });
    }

    init_select2();
    init_datepicker();
    init_wysihtml5();
});