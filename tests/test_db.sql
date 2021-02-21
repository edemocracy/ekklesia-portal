--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: argumenttype; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.argumenttype AS ENUM (
    'PRO',
    'CONTRA'
);


ALTER TYPE public.argumenttype OWNER TO ekklesia;

--
-- Name: majority; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.majority AS ENUM (
    'SIMPLE',
    'TWO_THIRDS'
);


ALTER TYPE public.majority OWNER TO ekklesia;

--
-- Name: propositionstatus; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.propositionstatus AS ENUM (
    'DRAFT',
    'SUBMITTED',
    'CHANGING',
    'ABANDONED',
    'QUALIFIED',
    'SCHEDULED',
    'VOTING',
    'FINISHED'
);


ALTER TYPE public.propositionstatus OWNER TO ekklesia;

--
-- Name: propositionvisibility; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.propositionvisibility AS ENUM (
    'PUBLIC',
    'UNLISTED',
    'HIDDEN'
);


ALTER TYPE public.propositionvisibility OWNER TO ekklesia;

--
-- Name: secretvoterstatus; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.secretvoterstatus AS ENUM (
    'ACTIVE',
    'EXPIRED',
    'RETRACTED'
);


ALTER TYPE public.secretvoterstatus OWNER TO ekklesia;

--
-- Name: supporterstatus; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.supporterstatus AS ENUM (
    'ACTIVE',
    'EXPIRED',
    'RETRACTED'
);


ALTER TYPE public.supporterstatus OWNER TO ekklesia;

--
-- Name: tsq_state; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.tsq_state AS (
	search_query text,
	parentheses_stack integer,
	skip_for integer,
	current_token text,
	current_index integer,
	current_char text,
	previous_char text,
	tokens text[]
);


ALTER TYPE public.tsq_state OWNER TO ekklesia;

--
-- Name: votebyuser; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.votebyuser AS ENUM (
    'UNSURE',
    'ACCEPT',
    'DECLINE',
    'ABSTENTION'
);


ALTER TYPE public.votebyuser OWNER TO ekklesia;

--
-- Name: votingstatus; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.votingstatus AS ENUM (
    'PREPARING',
    'SCHEDULED',
    'VOTING',
    'FINISHED',
    'ABORTED'
);


ALTER TYPE public.votingstatus OWNER TO ekklesia;

--
-- Name: votingsystem; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.votingsystem AS ENUM (
    'RANGE_APPROVAL'
);


ALTER TYPE public.votingsystem OWNER TO ekklesia;

--
-- Name: votingtype; Type: TYPE; Schema: public; Owner: ekklesia
--

CREATE TYPE public.votingtype AS ENUM (
    'ONLINE',
    'ASSEMBLY',
    'BOARD',
    'URN'
);


ALTER TYPE public.votingtype OWNER TO ekklesia;

--
-- Name: array_nremove(anyarray, anyelement, integer); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.array_nremove(anyarray, anyelement, integer) RETURNS anyarray
    LANGUAGE sql IMMUTABLE
    AS $_$
    WITH replaced_positions AS (
        SELECT UNNEST(
            CASE
            WHEN $2 IS NULL THEN
                '{}'::int[]
            WHEN $3 > 0 THEN
                (array_positions($1, $2))[1:$3]
            WHEN $3 < 0 THEN
                (array_positions($1, $2))[
                    (cardinality(array_positions($1, $2)) + $3 + 1):
                ]
            ELSE
                '{}'::int[]
            END
        ) AS position
    )
    SELECT COALESCE((
        SELECT array_agg(value)
        FROM unnest($1) WITH ORDINALITY AS t(value, index)
        WHERE index NOT IN (SELECT position FROM replaced_positions)
    ), $1[1:0]);
$_$;


ALTER FUNCTION public.array_nremove(anyarray, anyelement, integer) OWNER TO ekklesia;

--
-- Name: generate_ulid(); Type: FUNCTION; Schema: public; Owner: ts
--

CREATE FUNCTION public.generate_ulid() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
  -- Crockford's Base32
  encoding   BYTEA = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
  timestamp  BYTEA = E'\\000\\000\\000\\000\\000\\000';
  output     TEXT = '';

  unix_time  BIGINT;
  ulid       BYTEA;
BEGIN
  -- 6 timestamp bytes
  unix_time = (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT;
  timestamp = SET_BYTE(timestamp, 0, (unix_time >> 40)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 1, (unix_time >> 32)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 2, (unix_time >> 24)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 3, (unix_time >> 16)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 4, (unix_time >> 8)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 5, unix_time::BIT(8)::INTEGER);

  -- 10 entropy bytes
  ulid = timestamp || gen_random_bytes(10);

  -- Encode the timestamp
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 0) & 224) >> 5));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 0) & 31)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 1) & 248) >> 3));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 1) & 7) << 2) | ((GET_BYTE(ulid, 2) & 192) >> 6)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 2) & 62) >> 1));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 2) & 1) << 4) | ((GET_BYTE(ulid, 3) & 240) >> 4)));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 3) & 15) << 1) | ((GET_BYTE(ulid, 4) & 128) >> 7)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 4) & 124) >> 2));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 4) & 3) << 3) | ((GET_BYTE(ulid, 5) & 224) >> 5)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 5) & 31)));

  -- Encode the entropy
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 6) & 248) >> 3));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 6) & 7) << 2) | ((GET_BYTE(ulid, 7) & 192) >> 6)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 7) & 62) >> 1));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 7) & 1) << 4) | ((GET_BYTE(ulid, 8) & 240) >> 4)));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 8) & 15) << 1) | ((GET_BYTE(ulid, 9) & 128) >> 7)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 9) & 124) >> 2));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 9) & 3) << 3) | ((GET_BYTE(ulid, 10) & 224) >> 5)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 10) & 31)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 11) & 248) >> 3));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 11) & 7) << 2) | ((GET_BYTE(ulid, 12) & 192) >> 6)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 12) & 62) >> 1));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 12) & 1) << 4) | ((GET_BYTE(ulid, 13) & 240) >> 4)));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 13) & 15) << 1) | ((GET_BYTE(ulid, 14) & 128) >> 7)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 14) & 124) >> 2));
  output = output || CHR(GET_BYTE(encoding, ((GET_BYTE(ulid, 14) & 3) << 3) | ((GET_BYTE(ulid, 15) & 224) >> 5)));
  output = output || CHR(GET_BYTE(encoding, (GET_BYTE(ulid, 15) & 31)));

  RETURN output;
END
$$;


ALTER FUNCTION public.generate_ulid() OWNER TO ts;

--
-- Name: generate_uuid0(); Type: FUNCTION; Schema: public; Owner: ts
--

CREATE FUNCTION public.generate_uuid0() RETURNS uuid
    LANGUAGE plpgsql
    AS $$
DECLARE
  timestamp  BYTEA = E'\\000\\000\\000\\000\\000\\000';

  unix_time  BIGINT;
  bytes       BYTEA;
BEGIN
  -- 6 timestamp bytes
  unix_time = (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT;
  timestamp = SET_BYTE(timestamp, 0, (unix_time >> 40)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 1, (unix_time >> 32)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 2, (unix_time >> 24)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 3, (unix_time >> 16)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 4, (unix_time >> 8)::BIT(8)::INTEGER);
  timestamp = SET_BYTE(timestamp, 5, unix_time::BIT(8)::INTEGER);

  -- 10 entropy bytes
  bytes = timestamp || gen_random_bytes(10);


  RETURN bytes::uuid;
END
$$;


ALTER FUNCTION public.generate_uuid0() OWNER TO ts;

--
-- Name: propositions_search_vector_update(); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.propositions_search_vector_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                NEW.search_vector = (((setweight(to_tsvector('pg_catalog.german', coalesce(NEW.title, '')), 'A') || setweight(to_tsvector('pg_catalog.german', coalesce(NEW.abstract, '')), 'B')) || setweight(to_tsvector('pg_catalog.german', coalesce(NEW.content, '')), 'C')) || setweight(to_tsvector('pg_catalog.german', coalesce(NEW.motivation, '')), 'D')) || setweight(to_tsvector('pg_catalog.german', coalesce(NEW.voting_identifier, '')), 'A');
                RETURN NEW;
            END
            $$;


ALTER FUNCTION public.propositions_search_vector_update() OWNER TO ekklesia;

--
-- Name: tsq_append_current_token(public.tsq_state); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_append_current_token(state public.tsq_state) RETURNS public.tsq_state
    LANGUAGE plpgsql IMMUTABLE
    AS $$
BEGIN
    IF state.current_token != '' THEN
        state.tokens := array_append(state.tokens, state.current_token);
        state.current_token := '';
    END IF;
    RETURN state;
END;
$$;


ALTER FUNCTION public.tsq_append_current_token(state public.tsq_state) OWNER TO ekklesia;

--
-- Name: tsq_parse(text); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_parse(search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_parse(get_current_ts_config(), search_query);
$$;


ALTER FUNCTION public.tsq_parse(search_query text) OWNER TO ekklesia;

--
-- Name: tsq_parse(regconfig, text); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_parse(config regconfig, search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_process_tokens(config, tsq_tokenize(search_query));
$$;


ALTER FUNCTION public.tsq_parse(config regconfig, search_query text) OWNER TO ekklesia;

--
-- Name: tsq_parse(text, text); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_parse(config text, search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_parse(config::regconfig, search_query);
$$;


ALTER FUNCTION public.tsq_parse(config text, search_query text) OWNER TO ekklesia;

--
-- Name: tsq_process_tokens(text[]); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_process_tokens(tokens text[]) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
    SELECT tsq_process_tokens(get_current_ts_config(), tokens);
$$;


ALTER FUNCTION public.tsq_process_tokens(tokens text[]) OWNER TO ekklesia;

--
-- Name: tsq_process_tokens(regconfig, text[]); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_process_tokens(config regconfig, tokens text[]) RETURNS tsquery
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    result_query text;
    previous_value text;
    value text;
BEGIN
    result_query := '';

    FOREACH value IN ARRAY tokens LOOP
        IF value = '"' THEN
            CONTINUE;
        END IF;

        IF value = 'or' THEN
            value := ' | ';
        END IF;

        IF left(value, 1) = '"' AND right(value, 1) = '"' THEN
            value := phraseto_tsquery(config, value);
        ELSIF value NOT IN ('(', ' | ', ')', '-') THEN
            value := quote_literal(value) || ':*';
        END IF;

        IF previous_value = '-' THEN
            IF value = '(' THEN
                value := '!' || value;
            ELSIF value = ' | ' THEN
                CONTINUE;
            ELSE
                value := '!(' || value || ')';
            END IF;
        END IF;

        SELECT
            CASE
                WHEN result_query = '' THEN value
                WHEN previous_value = ' | ' AND value = ' | ' THEN result_query
                WHEN previous_value = ' | ' THEN result_query || ' | ' || value
                WHEN previous_value IN ('!(', '(') OR value = ')' THEN result_query || value
                WHEN value != ' | ' THEN result_query || ' & ' || value
                ELSE result_query
            END
        INTO result_query;

        IF result_query = ' | ' THEN
            result_query := '';
        END IF;

        previous_value := value;
    END LOOP;

    RETURN to_tsquery(config, result_query);
END;
$$;


ALTER FUNCTION public.tsq_process_tokens(config regconfig, tokens text[]) OWNER TO ekklesia;

--
-- Name: tsq_tokenize(text); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_tokenize(search_query text) RETURNS text[]
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    state tsq_state;
BEGIN
    SELECT
        search_query::text AS search_query,
        0::int AS parentheses_stack,
        0 AS skip_for,
        ''::text AS current_token,
        0 AS current_index,
        ''::text AS current_char,
        ''::text AS previous_char,
        '{}'::text[] AS tokens
    INTO state;

    state.search_query := lower(trim(
        regexp_replace(search_query, '""+', '""', 'g')
    ));

    FOR state.current_index IN (
        SELECT generate_series(1, length(state.search_query))
    ) LOOP
        state.current_char := substring(
            search_query FROM state.current_index FOR 1
        );

        IF state.skip_for > 0 THEN
            state.skip_for := state.skip_for - 1;
            CONTINUE;
        END IF;

        state := tsq_tokenize_character(state);
        state.previous_char := state.current_char;
    END LOOP;
    state := tsq_append_current_token(state);

    state.tokens := array_nremove(state.tokens, '(', -state.parentheses_stack);

    RETURN state.tokens;
END;
$$;


ALTER FUNCTION public.tsq_tokenize(search_query text) OWNER TO ekklesia;

--
-- Name: tsq_tokenize_character(public.tsq_state); Type: FUNCTION; Schema: public; Owner: ekklesia
--

CREATE FUNCTION public.tsq_tokenize_character(state public.tsq_state) RETURNS public.tsq_state
    LANGUAGE plpgsql IMMUTABLE
    AS $$
BEGIN
    IF state.current_char = '(' THEN
        state.tokens := array_append(state.tokens, '(');
        state.parentheses_stack := state.parentheses_stack + 1;
        state := tsq_append_current_token(state);
    ELSIF state.current_char = ')' THEN
        IF (state.parentheses_stack > 0 AND state.current_token != '') THEN
            state := tsq_append_current_token(state);
            state.tokens := array_append(state.tokens, ')');
            state.parentheses_stack := state.parentheses_stack - 1;
        END IF;
    ELSIF state.current_char = '"' THEN
        state.skip_for := position('"' IN substring(
            state.search_query FROM state.current_index + 1
        ));

        IF state.skip_for > 1 THEN
            state.tokens = array_append(
                state.tokens,
                substring(
                    state.search_query
                    FROM state.current_index FOR state.skip_for + 1
                )
            );
        ELSIF state.skip_for = 0 THEN
            state.current_token := state.current_token || state.current_char;
        END IF;
    ELSIF (
        state.current_char = '-' AND
        (state.current_index = 1 OR state.previous_char = ' ')
    ) THEN
        state.tokens := array_append(state.tokens, '-');
    ELSIF state.current_char = ' ' THEN
        state := tsq_append_current_token(state);
    ELSE
        state.current_token = state.current_token || state.current_char;
    END IF;
    RETURN state;
END;
$$;


ALTER FUNCTION public.tsq_tokenize_character(state public.tsq_state) OWNER TO ekklesia;

--
-- Name: uuid_timestamp(uuid); Type: FUNCTION; Schema: public; Owner: ts
--

CREATE FUNCTION public.uuid_timestamp(uuid uuid) RETURNS timestamp with time zone
    LANGUAGE plpgsql IMMUTABLE STRICT PARALLEL SAFE
    AS $$
DECLARE
  bytes bytea; 
BEGIN
  bytes := uuid_send(uuid);
  RETURN to_timestamp(
             (
                 (
                   (get_byte(bytes, 0)::bigint << 24) |
                   (get_byte(bytes, 1)::bigint << 16) |
                   (get_byte(bytes, 2)::bigint <<  8) |
                   (get_byte(bytes, 3)::bigint <<  0)
                 ) + (
                   ((get_byte(bytes, 4)::bigint << 8 |
                   get_byte(bytes, 5)::bigint)) << 32
                 ) + (
                   (((get_byte(bytes, 6)::bigint & 15) << 8 | get_byte(bytes, 7)::bigint) & 4095) << 48
                 ) - 122192928000000000
             ) / 10000 / 1000::double precision
         );
END
$$;


ALTER FUNCTION public.uuid_timestamp(uuid uuid) OWNER TO ts;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ekklesia;

--
-- Name: areamembers; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.areamembers (
    area_id integer NOT NULL,
    member_id integer NOT NULL
);


ALTER TABLE public.areamembers OWNER TO ekklesia;

--
-- Name: argumentrelations; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.argumentrelations (
    id integer NOT NULL,
    parent_id integer,
    argument_id integer,
    proposition_id bigint,
    argument_type public.argumenttype NOT NULL
);


ALTER TABLE public.argumentrelations OWNER TO ekklesia;

--
-- Name: COLUMN argumentrelations.parent_id; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.argumentrelations.parent_id IS 'only for inter-arguments';


--
-- Name: argumentrelations_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.argumentrelations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.argumentrelations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: arguments; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.arguments (
    id integer NOT NULL,
    title text NOT NULL,
    abstract text NOT NULL,
    details text,
    author_id integer,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.arguments OWNER TO ekklesia;

--
-- Name: arguments_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.arguments ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.arguments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: argumentvotes; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.argumentvotes (
    member_id integer NOT NULL,
    relation_id integer NOT NULL,
    weight integer NOT NULL
);


ALTER TABLE public.argumentvotes OWNER TO ekklesia;

--
-- Name: COLUMN argumentvotes.weight; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.argumentvotes.weight IS 'if extendedDiscussion: --(-2),-,0,+,++(+2) , otherwise -1 and +1';


--
-- Name: ballots; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.ballots (
    id integer NOT NULL,
    name text,
    election integer DEFAULT 0 NOT NULL,
    voting_type public.votingtype,
    proposition_type_id integer,
    area_id integer,
    voting_id integer,
    result jsonb
);


ALTER TABLE public.ballots OWNER TO ekklesia;

--
-- Name: ballots_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.ballots ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ballots_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: changeset; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.changeset (
    id integer NOT NULL,
    document_id integer NOT NULL,
    proposition_id bigint NOT NULL,
    section text
);


ALTER TABLE public.changeset OWNER TO ekklesia;

--
-- Name: COLUMN changeset.section; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.changeset.section IS 'Identifier for the section of the document that is changed.';


--
-- Name: changeset_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.changeset ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.changeset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: customizable_text; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.customizable_text (
    name text NOT NULL,
    lang text NOT NULL,
    text text,
    permissions json
);


ALTER TABLE public.customizable_text OWNER TO ekklesia;

--
-- Name: departmentmembers; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.departmentmembers (
    department_id integer NOT NULL,
    member_id integer NOT NULL,
    is_admin boolean DEFAULT false NOT NULL
);


ALTER TABLE public.departmentmembers OWNER TO ekklesia;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    exporter_settings jsonb DEFAULT '{}'::jsonb,
    voting_module_settings jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE public.departments OWNER TO ekklesia;

--
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.departments ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.departments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: document; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.document (
    id integer NOT NULL,
    name text,
    lang text,
    area_id integer,
    text text,
    description text,
    proposition_type_id integer
);


ALTER TABLE public.document OWNER TO ekklesia;

--
-- Name: document_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.document ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: groupmembers; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.groupmembers (
    group_id integer NOT NULL,
    member_id integer NOT NULL
);


ALTER TABLE public.groupmembers OWNER TO ekklesia;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name text NOT NULL,
    is_admin_group boolean DEFAULT false NOT NULL
);


ALTER TABLE public.groups OWNER TO ekklesia;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth_token; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.oauth_token (
    id integer NOT NULL,
    token json,
    provider text,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.oauth_token OWNER TO ekklesia;

--
-- Name: page; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.page (
    name text NOT NULL,
    lang text NOT NULL,
    title text,
    text text,
    permissions json
);


ALTER TABLE public.page OWNER TO ekklesia;

--
-- Name: policies; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.policies (
    id integer NOT NULL,
    name text NOT NULL,
    description text DEFAULT ''::text,
    majority public.majority,
    proposition_expiration integer,
    qualification_minimum integer,
    qualification_quorum numeric(3,2),
    range_max integer,
    range_small_max integer,
    range_small_options integer,
    secret_minimum integer,
    secret_quorum numeric(3,2),
    submitter_minimum integer,
    voting_duration integer,
    voting_system public.votingsystem
);


ALTER TABLE public.policies OWNER TO ekklesia;

--
-- Name: COLUMN policies.proposition_expiration; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.proposition_expiration IS 'days to reach the qualification (supporter) quorum';


--
-- Name: COLUMN policies.qualification_minimum; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.qualification_minimum IS 'minimum for qualification quorum';


--
-- Name: COLUMN policies.qualification_quorum; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.qualification_quorum IS 'fraction of area members that must support a proposition for reaching the qualified state';


--
-- Name: COLUMN policies.range_max; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.range_max IS 'maximum score used when the number of options is at least `range_small_options`';


--
-- Name: COLUMN policies.range_small_max; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.range_small_max IS 'maximum score used when the number of options is less than `range_small_options`';


--
-- Name: COLUMN policies.range_small_options; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.range_small_options IS 'largest number of options for which `range_small_max` is used as maximum score';


--
-- Name: COLUMN policies.secret_minimum; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.secret_minimum IS 'minimum for secret voting quorum';


--
-- Name: COLUMN policies.secret_quorum; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.secret_quorum IS 'quorum to force a secret voting';


--
-- Name: COLUMN policies.submitter_minimum; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.submitter_minimum IS 'minimum number of submitters for a proposition';


--
-- Name: COLUMN policies.voting_duration; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.policies.voting_duration IS 'voting duration in days; ends at target date';


--
-- Name: policies_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.policies ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.policies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: postalvotes; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.postalvotes (
    member_id integer NOT NULL,
    voting_id integer NOT NULL
);


ALTER TABLE public.postalvotes OWNER TO ekklesia;

--
-- Name: propositionnotes; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.propositionnotes (
    proposition_id bigint NOT NULL,
    user_id integer NOT NULL,
    notes text,
    vote public.votebyuser
);


ALTER TABLE public.propositionnotes OWNER TO ekklesia;

--
-- Name: propositions; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.propositions (
    id bigint NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    abstract text DEFAULT ''::text NOT NULL,
    motivation text DEFAULT ''::text NOT NULL,
    voting_identifier text,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    submitted_at timestamp without time zone,
    qualified_at timestamp without time zone,
    status public.propositionstatus DEFAULT 'DRAFT'::public.propositionstatus NOT NULL,
    submitter_invitation_key text,
    author_id integer,
    ballot_id integer NOT NULL,
    modifies_id bigint,
    replaces_id bigint,
    external_discussion_url text,
    external_fields jsonb DEFAULT '{}'::jsonb,
    visibility public.propositionvisibility DEFAULT 'PUBLIC'::public.propositionvisibility NOT NULL,
    search_vector tsvector,
    CONSTRAINT ck_propositions_qualified_at_must_be_set CHECK (((qualified_at IS NOT NULL) OR (status = ANY (ARRAY['DRAFT'::public.propositionstatus, 'SUBMITTED'::public.propositionstatus, 'ABANDONED'::public.propositionstatus, 'CHANGING'::public.propositionstatus, 'FINISHED'::public.propositionstatus])))),
    CONSTRAINT ck_propositions_submitted_at_must_be_set CHECK (((submitted_at IS NOT NULL) OR (status = ANY (ARRAY['DRAFT'::public.propositionstatus, 'ABANDONED'::public.propositionstatus, 'CHANGING'::public.propositionstatus]))))
);


ALTER TABLE public.propositions OWNER TO ekklesia;

--
-- Name: COLUMN propositions.submitted_at; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.propositions.submitted_at IS 'optional, §3.1, for order of voting §5.3, date of change if original (§3.4)';


--
-- Name: COLUMN propositions.qualified_at; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.propositions.qualified_at IS 'optional, when qualified';


--
-- Name: COLUMN propositions.modifies_id; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.propositions.modifies_id IS 'only one level allowed';


--
-- Name: COLUMN propositions.external_fields; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.propositions.external_fields IS 'Fields that are imported from or exported to other systems but are not interpreted by the portal.';


--
-- Name: propositiontags; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.propositiontags (
    proposition_id bigint NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.propositiontags OWNER TO ekklesia;

--
-- Name: propositiontypes; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.propositiontypes (
    id integer NOT NULL,
    name text NOT NULL,
    abbreviation text NOT NULL,
    description text DEFAULT ''::text,
    policy_id integer NOT NULL
);


ALTER TABLE public.propositiontypes OWNER TO ekklesia;

--
-- Name: propositiontypes_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.propositiontypes ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.propositiontypes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: secretvoters; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.secretvoters (
    member_id integer NOT NULL,
    ballot_id integer NOT NULL,
    status public.secretvoterstatus NOT NULL,
    last_change timestamp without time zone NOT NULL
);


ALTER TABLE public.secretvoters OWNER TO ekklesia;

--
-- Name: subjectareas; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.subjectareas (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    department_id integer NOT NULL
);


ALTER TABLE public.subjectareas OWNER TO ekklesia;

--
-- Name: subjectareas_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.subjectareas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.subjectareas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: supporters; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.supporters (
    member_id integer NOT NULL,
    proposition_id bigint NOT NULL,
    submitter boolean DEFAULT false NOT NULL,
    status public.supporterstatus DEFAULT 'ACTIVE'::public.supporterstatus NOT NULL,
    last_change timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.supporters OWNER TO ekklesia;

--
-- Name: COLUMN supporters.submitter; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.supporters.submitter IS 'submitter or regular';


--
-- Name: COLUMN supporters.last_change; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.supporters.last_change IS 'last status change';


--
-- Name: tags; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name text NOT NULL,
    parent_id integer,
    mut_exclusive boolean DEFAULT false NOT NULL
);


ALTER TABLE public.tags OWNER TO ekklesia;

--
-- Name: COLUMN tags.mut_exclusive; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.tags.mut_exclusive IS 'whether all children are mutually exclusive';


--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.tags ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: urns; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.urns (
    id integer NOT NULL,
    voting_id integer NOT NULL,
    accepted boolean DEFAULT false NOT NULL,
    location text NOT NULL,
    description text,
    opening time without time zone
);


ALTER TABLE public.urns OWNER TO ekklesia;

--
-- Name: urns_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.urns ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.urns_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: urnsupporters; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.urnsupporters (
    member_id integer NOT NULL,
    urn_id integer NOT NULL,
    type text NOT NULL,
    voted boolean DEFAULT false NOT NULL
);


ALTER TABLE public.urnsupporters OWNER TO ekklesia;

--
-- Name: user_login_token; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.user_login_token (
    token text NOT NULL,
    user_id integer,
    valid_until timestamp without time zone
);


ALTER TABLE public.user_login_token OWNER TO ekklesia;

--
-- Name: userpassword; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.userpassword (
    user_id integer NOT NULL,
    hashed_password text
);


ALTER TABLE public.userpassword OWNER TO ekklesia;

--
-- Name: userprofiles; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.userprofiles (
    id integer NOT NULL,
    sub text,
    eligible boolean,
    verified boolean,
    profile text
);


ALTER TABLE public.userprofiles OWNER TO ekklesia;

--
-- Name: users; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name text NOT NULL,
    email character varying(255),
    auth_type text DEFAULT 'system'::text NOT NULL,
    joined timestamp without time zone DEFAULT now() NOT NULL,
    active boolean DEFAULT true NOT NULL,
    last_active timestamp without time zone DEFAULT now() NOT NULL,
    can_login_until timestamp without time zone
);


ALTER TABLE public.users OWNER TO ekklesia;

--
-- Name: COLUMN users.email; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.users.email IS 'optional, for notifications, otherwise use user/mails/';


--
-- Name: COLUMN users.auth_type; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.users.auth_type IS 'deleted,system,token,virtual,oauth(has UserProfile)';


--
-- Name: COLUMN users.last_active; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.users.last_active IS 'last relevant activity (to be considered active member §2.2)';


--
-- Name: COLUMN users.can_login_until; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.users.can_login_until IS 'optional expiration datetime after which login is no longer possible';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: voting_module; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.voting_module (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    base_url text NOT NULL,
    module_type text NOT NULL
);


ALTER TABLE public.voting_module OWNER TO ekklesia;

--
-- Name: voting_module_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.voting_module ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.voting_module_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: voting_phase_types; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.voting_phase_types (
    id integer NOT NULL,
    name text DEFAULT ''::text,
    abbreviation text DEFAULT ''::text,
    secret_voting_possible boolean NOT NULL,
    voting_type public.votingtype NOT NULL
);


ALTER TABLE public.voting_phase_types OWNER TO ekklesia;

--
-- Name: COLUMN voting_phase_types.name; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.voting_phase_types.name IS 'readable name';


--
-- Name: COLUMN voting_phase_types.abbreviation; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.voting_phase_types.abbreviation IS 'abbreviated name';


--
-- Name: voting_phase_types_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.voting_phase_types ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.voting_phase_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: votingphases; Type: TABLE; Schema: public; Owner: ekklesia
--

CREATE TABLE public.votingphases (
    id integer NOT NULL,
    status public.votingstatus DEFAULT 'PREPARING'::public.votingstatus NOT NULL,
    target timestamp without time zone,
    department_id integer NOT NULL,
    phase_type_id integer NOT NULL,
    secret boolean DEFAULT false NOT NULL,
    name text DEFAULT ''::text,
    title text DEFAULT ''::text,
    description text DEFAULT ''::text,
    voting_module_data jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT ck_votingphases_state_valid CHECK ((((status = 'PREPARING'::public.votingstatus) AND (target IS NULL)) OR ((status <> 'PREPARING'::public.votingstatus) AND (target IS NOT NULL))))
);


ALTER TABLE public.votingphases OWNER TO ekklesia;

--
-- Name: COLUMN votingphases.target; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.votingphases.target IS 'constrained by §4.1';


--
-- Name: COLUMN votingphases.secret; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.votingphases.secret IS 'whether any secret votes will take place (decision deadline §4.2)';


--
-- Name: COLUMN votingphases.name; Type: COMMENT; Schema: public; Owner: ekklesia
--

COMMENT ON COLUMN public.votingphases.name IS 'short, readable name which can be used for URLs';


--
-- Name: votingphases_id_seq; Type: SEQUENCE; Schema: public; Owner: ekklesia
--

ALTER TABLE public.votingphases ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.votingphases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.alembic_version (version_num) FROM stdin;
e2ce064655e8
\.


--
-- Data for Name: areamembers; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.areamembers (area_id, member_id) FROM stdin;
1	2
2	2
4	3
1	4
\.


--
-- Data for Name: argumentrelations; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.argumentrelations (id, parent_id, argument_id, proposition_id, argument_type) FROM stdin;
1	\N	1	6769077249719871953	PRO
2	\N	2	6769077249719871953	PRO
3	\N	3	6769077249719871953	CONTRA
\.


--
-- Data for Name: arguments; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.arguments (id, title, abstract, details, author_id, created_at) FROM stdin;
1	Ein Pro-Argument	Die größte Überraschung war, wie schlecht die Debatte von den CNN-Moderatoren geleitet wurde. 15.33 Uhr: Gestern hatten Vidal und der FC Bay	11 Leserempfehlungen Man wollte nicht "in den Sumpf" hineingezogen werden, wiederholte Gabriel am Dienstag. 119,00 € incl. MwSt. zzgl. Versand Zum Shop Weitere Angebote vergleichen FritzBox 7430: Update auf FritzOS 6.26 verfügbar. 10 WINDOWS 10 Neues Betriebssystem im ersten Jahr als kostenloses Upgrade Kostenloses Upgrade: Im ersten Jahr können Windows 7 und 8.1 auf das neue Betriebssystem Windows 10 aktualisiert werden. 12:25 Uhr: EU-Parlamentspräsident Schulz warnt vor einem Zerfall Europas. 12> weiter Bewerten 8 0 Die mit * gekennzeichneten Felder sind Pflichtfelder. 1981 konnte man in Schkopau mit dem Aufstieg in die DDR-Oberliga den größten Erfolg der Vereinsgeschichte feiern. "1860 München wird kratzen, beißen, kämpfen, um aus der Abstiegszone wieder herauszukommen", weiß Lieberknecht. 12. Minute: Nächster Eckball für die Gastgeber, und plötzlich zappelt der Ball im Tor! 1989 wurde eine eigene Geschäftsstelle im Feuerwehrhaus Erbach in Betrieb genommen. 15m würden mir persönlich völlig ausreichen, mit dem heute üblichen schnick und schnack, kann man die auch noch zu zweit segeln und muß sich nicht mit Personal plagen.	2	2021-02-21 02:16:19.662801
2	Ein zweites Pro-Argument	dafür!!!	\N	3	2021-02-21 02:16:19.662801
3	Ein Contra-Argument	dagegen!!!	aus Gründen	2	2021-02-21 02:16:19.662801
\.


--
-- Data for Name: argumentvotes; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.argumentvotes (member_id, relation_id, weight) FROM stdin;
2	1	1
2	2	-1
3	1	-1
\.


--
-- Data for Name: ballots; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.ballots (id, name, election, voting_type, proposition_type_id, area_id, voting_id, result) FROM stdin;
1	PP001/2/3/4	0	\N	1	2	1	\N
2	\N	0	\N	1	2	\N	\N
3	\N	0	\N	1	2	\N	\N
4	\N	0	\N	1	2	\N	\N
5	\N	0	\N	1	2	\N	\N
6	\N	0	\N	1	2	\N	\N
7	PP001	0	\N	1	1	3	{"PP001": {"no": 10, "yes": 14, "rank": 1, "points": 213, "abstention": 15}}
8	PP005	0	\N	1	1	3	{"PP005": {"state": "accepted"}}
9	PP006	0	\N	1	1	3	{"PP006": {"state": "rejected"}}
10	PP007/8	0	\N	1	1	3	{"PP007": {"state": "not decided"}, "PP008": {"state": "rejected"}}
\.


--
-- Data for Name: changeset; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.changeset (id, document_id, proposition_id, section) FROM stdin;
\.


--
-- Data for Name: customizable_text; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.customizable_text (name, lang, text, permissions) FROM stdin;
push_draft_external_template	de	\nDieser Antragsentwurf wurde automatisch erstellt durch das Antragsportal\n\n{draft_link}\n\n## Vorbemerkungen / Bearbeitungshinweise\n\n(nicht Teil des Antrags)\n\n{editing_remarks}\n\n## Zusammenfassung\n\n{abstract}\n\n## Antragstext\n\n{content}\n\n## Begründung\n\n{motivation}\n	\N
push_draft_portal_template	de	\nDer Antragsentwurf wird hier weiterentwickelt:\n\n{topic_url}\n\nVerbesserungsvorschläge und Verständnisfragen bitte dort einbringen.\n	\N
document_propose_change_explanation	de	\nStelle einen Wahlprogrammantrag, um dieses Programm zu ändern.\nDu kannst eine Änderung an einem Abschnitt vorschlagen, indem du auf dessen Überschrift klickst.\nAuf der folgenden Seite kannst du den Text bearbeiten und weitere Informationen zu deinen Antragsentwurf ergänzen.\n	\N
new_draft_explanation	de	\nNach dem Abschicken wird dein Antragsentwurf automatisch im Forum in der Kategorie Antragsentwicklung eingestellt.\nDer Text des Antrags kann dort von allen angemeldeten Benutzern bearbeitet werden wie in einem Wiki.\nDu kannst die Bearbeitung sperren lassen. Wende dich dazu an die Antragskommission.\n	\N
\.


--
-- Data for Name: departmentmembers; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.departmentmembers (department_id, member_id, is_admin) FROM stdin;
3	2	f
4	2	f
3	4	t
5	3	f
\.


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.departments (id, name, description, exporter_settings, voting_module_settings) FROM stdin;
1	Landesverband Bayern	\N	{}	{}
2	Bezirksverband Oberpfalz	\N	{}	{}
3	Piratenpartei Deutschland	\N	{"exporter_name": "testdiscourse", "exporter_description": "Ein Test-Discourse"}	{}
4	Piratenpartei Schweiz	\N	{}	{}
5	Zentralschweiz	\N	{}	{}
\.


--
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.document (id, name, lang, area_id, text, description, proposition_type_id) FROM stdin;
1	Wahlprogramm	de	1	# Wahlprogramm\n\n## Section 1 {data-section="1"}\n\n### Section 1.1 {data-section="1.1"}\n\nText Section 1.1\n	Ein Wahlprogramm	2
\.


--
-- Data for Name: groupmembers; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.groupmembers (group_id, member_id) FROM stdin;
1	1
2	2
2	3
2	4
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.groups (id, name, is_admin_group) FROM stdin;
1	Göttliche Admins	t
2	Deppengruppe	f
\.


--
-- Data for Name: oauth_token; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.oauth_token (id, token, provider, created_at) FROM stdin;
3	{}	ekklesia	2021-02-21 02:16:19.662801
4	{}	ekklesia	2021-02-21 02:16:19.662801
\.


--
-- Data for Name: page; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.page (name, lang, title, text, permissions) FROM stdin;
\.


--
-- Data for Name: policies; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.policies (id, name, description, majority, proposition_expiration, qualification_minimum, qualification_quorum, range_max, range_small_max, range_small_options, secret_minimum, secret_quorum, submitter_minimum, voting_duration, voting_system) FROM stdin;
1	default	1c) Das EZB-QE falscher Machart reduziert die Renditen weiter. 18:22 Wie UBM, PIAG Immobilien, AT&S, Frauenthal, Warimpex und DO&CO für Gesprächsstoff in Österreich sorgten Das hat die BSNgine heute ausgewiesen FKA: Frauenthal am 13.2. 13.31 Uhr: Niersbach erklärt, er "zermartere" sich den Kopf: "Was ist denn damals gewesen?"	SIMPLE	180	50	0.10	9	3	5	20	0.05	2	14	RANGE_APPROVAL
\.


--
-- Data for Name: postalvotes; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.postalvotes (member_id, voting_id) FROM stdin;
\.


--
-- Data for Name: propositionnotes; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.propositionnotes (proposition_id, user_id, notes, vote) FROM stdin;
\.


--
-- Data for Name: propositions; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.propositions (id, title, content, abstract, motivation, voting_identifier, created_at, submitted_at, qualified_at, status, submitter_invitation_key, author_id, ballot_id, modifies_id, replaces_id, external_discussion_url, external_fields, visibility, search_vector) FROM stdin;
6769077249719871953	Ein Titel	13:45 dpa-AFX: NordLB belässt Allianz SE auf 'Halten' - Ziel 152 Euro 11.08. 11.11 Uhr - Datendienst bei Vodafone gestört: Bei Twitter berichteten Nutzer von einer Vodafone-Netzstörung in Berlin. 19:39 Ansonsten bleibt die Elf unverändert - das heißt, dass auch Debütant Can direkt wieder von Beginn an ran darf. 16 Bilder Ein Blick in diese Augen, und du bist verliebt. 1977 hatte Harrison Ford Han Solo verkörpert und wurde mit dieser Rolle weltberühmt. 17 Spiele, 14 Punkte, letzter Platz: Die Bilanz unter Sami Hyypiä ist miserabel. 12.25 Uhr: "Wir werden uns um 16 Uhr mit den Fans treffen, um gemeinsam Abschied zu nehmen", sagt Allofs. "1,3 Millionen Euro sind insgesamt dafür vorgesehen", so Landesrätin Doris Kampus (SPÖ). 14.41 Uhr Die Verantwortlichen der Nasa stellen sich den Fragen der anwesenden Journalisten. 19:08 Uhr Lauda ist zurück Niki Lauda wieder einmal ans Steuer eines Formel-1-Boliden. 16:37 Jositsch im ersten Wahlgang gewählt Laut Hochrechnung schafft SP-Kandidat Daniel Jositsch bereits im ersten Wahlgang den Sprung in den Ständerat. 17. September 2015 08:34 Apple-Betriebssystem iOS 9-Update sorgt für Mega-Frust User klagen über fehlgeschlagene Updates und Serverüberlastung. 12. September 2015 18:11 Russische Flugzeuge in Syrien gelandet Merkel: Ohne Zusammenarbeit mit Russland kein Ende des Bürgerkriegs. 11.01.15 Altlasten aus dem Jahr 1942 Deutschland soll Athen Milliarden schulden 10.01.15 Neue Pläne für Griechenland? 13,5 Prozent der Unternehmergesellschaften (haftungsbeschränkt) droht eine Insolvenz. 11:19 Leoni AG: Kreuzen des GD 50 nach unten (58.7 Euro, Short) 13.07. 17 Leserempfehlungen Reaktionen auf diesen Kommentar anzeigen Austeritätspolitik ist gescheitert. 19:52 DGAP-Adhoc: SNP AG gewinnt internationales SAP-Projekt bei bedeutendem US-amerikanischen Computer- und IT-Unternehmen (deutsch) 30.01. 12:22 UBS belässt ARM auf 'Buy' - Ziel 1200 Pence Die Schweizer Großbank UBS hat die Einstufung für ARM nach einer Investorenveranstaltung auf "Buy" mit einem Kursziel von 1200 Pence belassen. 10 Leserempfehlungen Antwort auf "Wie kommt es?" 13-mal am Tag im Westside Auch bei Pathé-Westside-Chef Jan Halvorsen ist die Vorfreude auf «Spectre» riesig. 15.09.2017 13:44 Uhr Dennis Schirrmacher vorlesen Das Let's-Encrypt-Projekt hat eine Webseite live geschaltet, die auf das erste Zertifikat der alternativen Zertifizierungsstelle setzt. 10:06 Uhr - Kauder: Es gibt viele Gründe, dem Antrag zuzustimmen. 13:40 Uhr - Demonstrationsverbot in Paris verlängert: Das Demonstrationsverbot nach den Terroranschlägen in Paris ist bis Ende November verlängert worden. 11.14 Uhr: Sport- und Innensenator Michael Neumann sagt auf dem HSV-Neujahrsempfang: „Super, das Volksparkstadion heißt auch offiziell wieder so. Ein tolles Zeichen. 1 Absturz der Germanwings-Maschine War die Freundin des Todes-Piloten.. 10 Leserempfehlungen 6. Ich will mich abgrenzen Jan Fleischhauer schreibt im Spiegel: Eigenartigerweise verspricht gerade der nahrungstechnische Luxuskonsum moralischen Mehrwert. 17:01 DGAP-AFR: Henkel AG & Co. KGaA: Bekanntmachung gemäß § 37v, 37w, 37x ff. WpHG mit dem Ziel der europaweiten Verbreitung 03.02. Im Komplex Ahrensburg/Ahrensfelde" konnte eine Gruppe von vier Feuerwehrleuten ausgemacht werden, denen nunmehr neun Brandlegungen zur Last gelegt werden. 1 Jahr zum Kursportrait AdHoc-Meldungen & Insidertrades Werbung Nachrichten zu ELEKTR. 13 Leserempfehlungen Reaktionen auf diesen Kommentar anzeigen "Wo lebt der Autor?" 12 Leserempfehlungen Reaktionen auf diesen Kommentar anzeigen Entfernt. 09. Jänner 2015 21:43 Hollande: Islamistische Bedrohung besteht fort Premier: Präsident entschied selbst über Doppelschlag der Polizei. 16:05 Von Anfang an macht Real Madrid gehörig Druck. 13 Tore mehr Der FCZ kann mit der Europa-League-Qualifikation planen. 09:21 - International Heidi kämpft gegen Kopfläuse 06:32 - International Wer lügt? 11:45Berater: Kein Sane-Wechsel im Winter Schalke-Talent Leroy Sane wird die Saison 2015/16 nach Angaben seines Beraters Jürgen Milewski beim FC Schalke 04 beenden. 17.08.2017 20:01 Uhr Jörg Wirtgen vorlesen Google hat die finale Version des SDKs für Android M herausgebracht und nebenher zwei Details verraten: Diese Version wird Android 6.0 Marshmallow heißen. 1 Diesmal mit Höschen Dänen-Kickerinnen PO-sieren am Strand 2 Federer hilft in Malawi Messi lässt sich von Gabun-Diktator kaufen 3 Das war nix! 13 Leserempfehlungen Reaktionen auf diesen Kommentar anzeigen Ich fürchte die € Zone wählt den Grexit nicht.			PP001	2020-01-01 00:00:00	2020-01-05 00:00:00	2020-01-08 00:00:00	SCHEDULED	\N	\N	1	\N	\N	http://example.com	{}	PUBLIC	'-1':151C '..':445C '01':467C,622C '03.02':488C '04':618C '05':558C '06':378C,587C '08':138C,180C '09':539C,580C '1':111C,432C,508C,650C '10':323C,377C,446C '10.01.15':230C '11':204C,244C,592C '11.01.15':219C '11.08':17C '11.11':18C '11.14':408C '12':200C,292C,531C '12.25':92C '1200':300C,320C '13':3C,235C,330C,351C,388C,520C,567C,679C '13.07':257C '14':81C '14.41':124C '15.09.2017':350C '152':15C '16':55C,98C,153C,557C '17':79C,177C,258C,466C '17.08.2017':620C '18':203C '19':35C,137C,245C,268C '1942':224C '1977':66C '2':662C '20':621C '2015':179C,202C,541C '2015/16':608C '21':542C,581C '22':293C '3':112C,675C '30.01':291C '32':588C '34':181C '37':154C '37v':477C '37w':478C '37x':479C '39':36C '40':389C '43':543C '44':352C '45':4C '45berater':593C '5':236C '50':251C '52':269C '58.7':254C '6':448C '6.0':647C '9':186C 'abgrenz':452C 'abschied':106C 'absturz':433C 'adhoc':272C,513C 'adhoc-meld':512C 'afr':470C 'afx':7C 'ag':247C,274C,472C 'ahrensburg/ahrensfelde':491C 'allianz':10C 'allof':110C 'alternativ':374C 'altlast':220C 'amerikan':284C 'android':635C,646C 'anfang':560C 'angab':610C 'ans':147C 'anson':37C 'antrag':386C 'antwort':325C 'anwes':135C 'anzeig':264C,526C,537C,685C 'appl':183C 'apple-betriebssyst':182C 'arm':296C,310C 'ath':227C 'aug':61C 'ausgemacht':498C 'austeritatspolit':265C 'autor':530C 'bedeut':281C 'bedroh':546C 'beend':619C 'beginn':51C 'beim':615C 'bekanntmach':475C 'belass':322C 'belasst':9C,295C 'berat':612C 'bereit':168C 'berichtet':26C 'berlin':34C 'besteht':547C 'betriebssyst':184C 'bilanz':86C 'bild':56C 'bleibt':38C 'blick':58C 'bolid':152C 'brandleg':503C 'burgerkrieg':218C 'buy':298C,315C 'can':47C 'chef':341C 'co':473C 'comput':285C 'dafur':117C 'dan':655C 'danen-kickerinn':654C 'daniel':166C 'darf':54C 'dass':44C 'datendien':20C 'debutant':46C 'demonstrationsverbot':391C,396C 'den':500C 'dennis':354C 'detail':641C 'deutsch':290C 'deutschland':225C 'dgap':271C,469C 'dgap-adhoc':270C 'dgap-afr':468C 'diesmal':651C 'diktator':673C 'direkt':48C 'doppelschlag':554C 'doris':121C 'dpa':6C 'dpa-afx':5C 'droht':241C 'druck':566C 'eigenartigerweis':458C 'einstuf':308C 'elektr':519C 'elf':40C 'encrypt':361C 'end':216C,404C 'entfernt':538C 'entschied':551C 'erst':157C,170C,371C 'euro':16C,114C,255C 'europa':576C 'europa-league-qualifikation':575C 'europaweit':486C 'fan':102C 'fc':616C 'fcz':571C 'fed':663C 'fehlgeschlag':196C 'feuerwehrleut':497C 'ff':480C 'final':630C 'fleischhau':454C 'flugzeug':206C 'ford':69C 'formel':150C 'fort':548C 'frag':133C 'freundin':440C 'frust':192C 'furcht':687C 'gabun':672C 'gabun-diktator':671C 'gd':250C 'gehor':565C 'gelandet':209C 'gelegt':506C 'gemass':476C 'gemeinsam':105C 'gerad':460C 'germanwing':436C 'germanwings-maschin':435C 'geschaltet':367C 'gescheitert':267C 'gestort':23C 'gewahlt':159C 'gewinnt':275C 'gibt':382C 'googl':627C 'grexit':692C 'griechenland':234C 'grossbank':304C 'grund':384C 'grupp':494C 'haftungsbeschrankt':240C 'halt':13C 'halvors':343C 'han':70C 'harrison':68C 'heidi':583C 'heiss':649C 'heisst':43C,424C 'henkel':471C 'herausgebracht':637C 'hilft':664C 'hochrechn':161C 'holland':544C 'hosch':653C 'hsv':419C 'hsv-neujahrsempfang':418C 'hyypia':89C 'innensenator':412C 'insgesamt':116C 'insidertrad':515C 'insolvenz':243C 'international':276C,582C,589C 'investorenveranstalt':313C 'ios':185C 'islamist':545C 'it':288C 'it-unternehm':287C 'jahr':223C,509C 'jan':342C,453C 'jann':540C 'jorg':624C 'jositsch':155C,167C 'journalist':136C 'jurg':613C 'kampft':584C 'kampus':122C 'kandidat':165C 'kaud':380C 'kauf':674C 'kgaa':474C 'kickerinn':656C 'klag':194C 'kommentar':263C,525C,536C,684C 'kommt':328C 'komplex':490C 'konnt':492C 'kopflaus':586C 'kreuz':248C 'kursportrait':511C 'kursziel':318C 'landesratin':120C 'lasst':668C 'last':505C 'lauda':140C,144C 'laut':160C 'leagu':577C 'lebt':528C 'leoni':246C 'leroy':603C 'leserempfehl':259C,324C,447C,521C,532C,680C 'let':358C 'letzt':83C 'liv':366C 'lugt':591C 'luxuskonsum':463C 'm':636C 'macht':562C 'madrid':564C 'mal':331C 'malawi':666C 'marshmallow':648C 'maschin':437C 'mega':191C 'mega-frust':190C 'mehr':569C 'mehrwert':465C 'meldung':514C 'merkel':210C 'messi':667C 'michael':413C 'milewski':614C 'milliard':228C 'million':113C 'miserabel':91C 'moral':464C 'nachricht':517C 'nahrungstechn':462C 'nasa':129C 'nebenh':639C 'nehm':108C 'netzstor':32C 'neu':231C 'neujahrsempfang':420C 'neumann':414C 'neun':502C 'niki':143C 'nix':678C 'nordlb':8C 'novemb':405C 'nunmehr':501C 'nutz':27C 'offiziell':426C 'paris':393C,401C 'pathé':339C 'pathé-westside-chef':338C 'penc':301C,321C 'pilot':444C 'plan':232C,579C 'platz':84C 'po':658C 'po-si':657C 'polizei':556C 'pp001':693A 'prasident':550C 'premi':549C 'projekt':279C,362C 'prozent':237C 'punkt':82C 'qualifikation':578C 'ran':53C 'reaktion':260C,522C,533C,681C 'real':563C 'riesig':349C 'roll':77C 'russisch':205C 'russland':214C 's':360C 's-encrypt-projekt':359C 'sagt':109C,415C 'saison':607C 'sami':88C 'san':596C,604C 'sane-wechsel':595C 'sap':278C 'sap-projekt':277C 'schafft':162C 'schalk':601C,617C 'schalke-talent':600C 'schirrmach':355C 'schreibt':455C 'schuld':229C 'schweiz':303C 'sdks':633C 'se':11C 'septemb':178C,201C 'serveruberlast':199C 'setzt':376C 'short':256C 'sier':659C 'snp':273C 'solo':71C 'sorgt':188C 'sp':164C 'sp-kandidat':163C 'spectr':348C 'spiegel':457C 'spiel':80C 'spo':123C 'sport':410C 'sprung':173C 'standerat':176C 'stell':130C 'steu':148C 'strand':661C 'sup':421C 'syri':208C 'tag':333C 'talent':602C 'terroranschlag':399C 'titel':2A 'tod':443C 'todes-pilot':442C 'toll':430C 'tor':568C 'treff':103C 'twitt':25C 'ubs':294C,305C 'uhr':19C,93C,99C,125C,139C,353C,379C,390C,409C,623C 'unt':253C 'unternehm':289C 'unternehmergesellschaft':239C 'unverandert':41C 'updat':187C,197C 'us':283C 'us-amerikan':282C 'user':193C 'verantwort':127C 'verbreit':487C 'verkorpert':72C 'verlangert':394C,406C 'verliebt':65C 'verrat':642C 'version':631C,644C 'verspricht':459C 'viel':383C 'vier':496C 'vodafon':22C,31C 'vodafone-netzstor':30C 'volksparkstadion':423C 'vorfreud':346C 'vorgeseh':118C 'vorles':356C,626C 'wahlgang':158C,171C 'wahlt':690C 'webseit':365C 'wechsel':597C 'weltberuhmt':78C 'wer':590C 'werbung':516C 'westsid':335C,340C 'wint':599C 'wirtg':625C 'word':407C 'wphg':481C 'wurd':74C 'zeich':431C 'zertifikat':372C 'zertifizierungsstell':375C 'ziel':14C,299C,484C 'zon':689C 'zuruck':142C 'zusammenarbeit':212C 'zuzustimm':387C 'zwei':640C
6769077249737786120	Fallengelassener Antrag	Einfach so fallengelassen...			\N	2020-01-01 00:00:00	\N	\N	ABANDONED	\N	\N	2	\N	\N	http://example.com	{}	PUBLIC	'antrag':2A 'einfach':3C 'fallengelass':1A,5C
6769077249744553781	Sich ändernder Antrag	Einfach so ändernd...			\N	2020-01-01 00:00:00	\N	\N	CHANGING	\N	\N	3	\N	\N	http://example.com	{}	PUBLIC	'andernd':2A,6C 'antrag':3A 'einfach':4C
6769077249745788325	Entstehender Antrag	Einfach so entstehend...			\N	2020-01-06 00:00:00	\N	\N	DRAFT	\N	2	4	\N	\N	\N	{}	PUBLIC	'antrag':2A 'einfach':3C 'entsteh':1A,5C
6769077249745559767	Übertragener Antrag	Einfach so Übertragen...			\N	2020-01-06 00:00:00	2020-01-06 00:00:00	\N	SUBMITTED	\N	\N	5	\N	\N	http://example.com	{}	PUBLIC	'antrag':2A 'einfach':3C 'ubertrag':1A,5C
6769077249753597599	Qualifizierter Antrag	Einfach so qualifiziert...			\N	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	QUALIFIED	\N	\N	6	\N	\N	\N	{}	PUBLIC	'antrag':2A 'einfach':3C 'qualifiziert':1A,5C
6769077249757422710	Antrag mit nicht unterstütztem Ergebnisformat	10:08 DGAP-Adhoc: nebag ag: Provisorisch berechneter innerer Wert pro Aktie per 3Dezember 2014 beträgt CHF 9.95 (Performance von 7.38% inkl. Ausschüttung) 01.12. Plötzlich erblickte er den schmalen Durchgang. 1962 schaffte sich die Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU) die Rechenanlage ZUSE Z23 an und nutzte sie bis in die 70er Jahre. 12910198 Kevin Kuranyi: „Russisches Sommermärchen“ WM 2018 – warum nicht? 1985 - Die UdSSR unterzeichnet Abkommen mit der Internationalen Atomenergiebehörde über die Kontrolle ihrer zivilen Kernanlagen. 10. Sahne mit Vanillezucker steif schlagen, etwas davon in einen Spritzbeutel geben und den Rest oben auf die Torte streichen. Das bedeutete nichts Gutes. 17:19 Uhr Hamilton jagt den nächsten Rekord Gewinnt der Weltmeister am Sonntag auf dem Hungaroring, wäre er der erste Fahrer, dem dieses Kunststück fünfmal gelingt. 10. Deutschlands Kriegsschulden wurden im Londoner Schuldenabkommen von 1953 zum großen Teil erlassen. ¹ Fast 2500 Schulen sind geschlossen. “ 12. Januar 2015 um 06:07 Ein Chef der beschriebenen Sorte interessiert sich einen feuchten Staub ob man eine Wut im Bauch hat. 09:43 Commerzbank hebt Rhön-Klinikum auf 'Buy' und Ziel auf 30 Euro Die Commerzbank hat Rhön-Klinikum von "Hold" auf "Buy" hochgestuft und das Kursziel von 25 auf 30 Euro angehoben. " 18 Leserempfehlungen Reaktionen auf diesen Kommentar anzeigen versteht exakt alles! 13.30 Uhr: Der Dax Börsen-Chart zeigen baut angesichts einer nahenden Staatspleite Griechenlands seine Verluste auf 0,6 Prozent aus und fällt wieder unter die Marke von 11.000 Punkten. 10:35 Das ist nur der fünfte und letzte Platz für die Tina - Über eine halbe Sekunde Rückstand! 1999 in Karlsruhe: Eine Frau und zwei Männer erwarten gespannt mit Schutzbrillen die totale Sonnenfinsternis. 14. 2014 legte der Toyota TS040-Hybrid mit Davidson, Sebastien Buemi und Nicolas Lapierre 1197,67 km (171 Runden) zurück. 11:52Mustafi droht längere Zwangspause Nationalspieler Shkodran Mustafi droht wegen einer Muskelverletzung eine längere Zwangspause. 1 2 weiter » Hill das ist schon ungefähr der 10. teaser den sie veröffentlichen aber sie releasen einfach nichts. 160 statt 80 km/h Vater rast mit Sohn (6) auf dem Töff Raser Patrice M. (29) hatte nicht mal das Billett Mit 135 Km/h durch Hägendorf Bundesgericht verfügt Zug muss Raser 2000 Fr zahlen!			PP001	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	FINISHED	\N	\N	7	\N	\N	http://example.com	{}	PUBLIC	'0':238C '01.12':30C '06':158C '07':159C '08':7C '09':177C '1':320C '10':6C,86C,136C,251C,329C '11':305C '11.000':249C '1197':299C '12':154C '12910198':62C '13.30':221C '135':361C '14':284C '160':339C '17':110C '171':302C '18':211C '19':111C '1953':144C '1962':37C '1985':71C '1999':269C '2':321C '2000':370C '2014':21C,285C '2015':156C '2018':68C '25':206C '2500':150C '29':354C '30':189C,208C '35':252C '3dezember':20C '43':178C '52mustafi':306C '6':239C,347C '67':300C '7.38':27C '70er':60C '80':341C '9.95':24C 'abkomm':75C 'adhoc':10C 'ag':12C 'akti':18C 'alexand':43C 'angehob':210C 'angesicht':230C 'antrag':1A 'anzeig':217C 'atomenergiebehord':79C 'ausschutt':29C 'bauch':175C 'baut':229C 'bedeutet':107C 'berechnet':14C 'beschrieb':163C 'betragt':22C 'billett':359C 'bors':226C 'borsen-chart':225C 'buemi':295C 'bundesgericht':365C 'buy':185C,200C 'chart':227C 'chef':161C 'chf':23C 'commerzbank':179C,192C 'davidson':293C 'davon':93C 'dax':224C 'deutschland':137C 'dgap':9C 'dgap-adhoc':8C 'droht':307C,313C 'durchgang':36C 'einfach':337C 'erblickt':32C 'ergebnisformat':5A 'erlang':46C 'erlangen-nurnberg':45C 'erlass':148C 'erst':129C 'erwart':277C 'euro':190C,209C 'exakt':219C 'fahr':130C 'fallt':243C 'fast':149C 'fau':48C 'feucht':168C 'fr':371C 'frau':273C 'friedrich':42C 'friedrich-alexander-universitat':41C 'funfmal':134C 'funft':257C 'geb':97C 'gelingt':135C 'geschloss':153C 'gespannt':278C 'gewinnt':118C 'griechenland':234C 'gross':146C 'gut':109C 'hagendorf':364C 'halb':266C 'hamilton':113C 'hebt':180C 'hill':323C 'hochgestuft':201C 'hold':198C 'hungaroring':125C 'hybrid':291C 'inkl':28C 'inn':15C 'interessiert':165C 'international':78C 'jagt':114C 'jahr':61C 'januar':155C 'karlsruh':271C 'kernanlag':85C 'kevin':63C 'klinikum':183C,196C 'km':301C 'km/h':342C,362C 'kommentar':216C 'kontroll':82C 'kriegsschuld':138C 'kunststuck':133C 'kuranyi':64C 'kursziel':204C 'lang':308C,318C 'lapierr':298C 'legt':286C 'leserempfehl':212C 'letzt':259C 'london':141C 'm':353C 'mal':357C 'mann':276C 'mark':247C 'muskelverletz':316C 'mustafi':312C 'nach':116C 'nahend':232C 'nationalspiel':310C 'nebag':11C 'nicolas':297C 'nurnberg':47C 'nutzt':55C 'oben':101C 'patric':352C 'per':19C 'performanc':25C 'platz':260C 'plotzlich':31C 'pp001':373A 'pro':17C 'provisor':13C 'prozent':240C 'punkt':250C 'ras':351C,369C 'rast':344C 'reaktion':213C 'rechenanlag':50C 'rekord':117C 'releas':336C 'rest':100C 'rhon':182C,195C 'rhon-klinikum':181C,194C 'ruckstand':268C 'rund':303C 'russisch':65C 'sahn':87C 'schafft':38C 'schlag':91C 'schmal':35C 'schon':326C 'schul':151C 'schuldenabkomm':142C 'schutzbrill':280C 'sebasti':294C 'sekund':267C 'shkodran':311C 'sohn':346C 'sommermarch':66C 'sonnenfinsternis':283C 'sonntag':122C 'sort':164C 'spritzbeutel':96C 'staatspleit':233C 'statt':340C 'staub':169C 'steif':90C 'streich':105C 'teas':330C 'teil':147C 'tina':263C 'toff':350C 'tort':104C 'total':282C 'toyota':288C 'ts040':290C 'ts040-hybrid':289C 'udssr':73C 'uhr':112C,222C 'ungefahr':327C 'universitat':44C 'unterstutzt':4A 'unterzeichnet':74C 'vanillezuck':89C 'vat':343C 'verfugt':366C 'verlust':236C 'veroffent':333C 'versteht':218C 'war':126C 'warum':69C 'weg':314C 'weltmeist':120C 'wert':16C 'wm':67C 'wurd':139C 'wut':173C 'z23':52C 'zahl':372C 'zeig':228C 'ziel':187C 'zivil':84C 'zug':367C 'zuruck':304C 'zus':51C 'zwangspaus':309C,319C 'zwei':275C
6769077249765775280	Angenommener Antrag	12:01 Uhr - FAW-Volkswagen und Shanghai Volkswagen, zwei chinesische Volkswagen-Joint-Ventures, haben erklärt, vom Skandal um manipulierte Abgaswerte nicht betroffen zu sein. 13:55Auch Barmer Ersatzkasse erhöht Zusatzbeitrag Der Beitragssatz der Barmer GEK steigt im kommenden Jahr auf 15,7 Prozent.			PP005	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	FINISHED	\N	\N	8	\N	\N	http://example.com	{}	PUBLIC	'01':4C '12':3C '13':29C '15':45C '55auch':30C '7':46C 'abgaswert':24C 'angenomm':1A 'antrag':2A 'barm':31C,38C 'beitragssatz':36C 'betroff':26C 'chines':13C 'erhoht':33C 'erklart':19C 'ersatzkass':32C 'faw':7C 'faw-volkswag':6C 'gek':39C 'jahr':43C 'joint':16C 'kommend':42C 'manipuliert':23C 'pp005':48A 'prozent':47C 'shanghai':10C 'skandal':21C 'steigt':40C 'uhr':5C 'ventur':17C 'volkswag':8C,11C,15C 'volkswagen-joint-ventur':14C 'zusatzbeitrag':34C 'zwei':12C
6769077249768528865	Abgelehnter Antrag	Bla			PP006	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	FINISHED	\N	\N	9	\N	\N	http://example.com	{}	PUBLIC	'abgelehnt':1A 'antrag':2A 'bla':3C 'pp006':4A
6769077249766705726	Verschobener Antrag	Blubb			PP007	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	FINISHED	\N	\N	10	\N	\N	http://example.com	{}	PUBLIC	'antrag':2A 'blubb':3C 'pp007':4A 'verschob':1A
6769077249776842760	Änderungsantrag zu PP001	will was ändern			PP004	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	SCHEDULED	\N	\N	1	6769077249719871953	\N	\N	{}	PUBLIC	'and':6C 'anderungsantrag':1A 'pp001':3A 'pp004':7A
6769077249780739847	Gegenantrag zu PP001	will was anderes			PP002	2020-01-02 00:00:00	2020-01-07 00:00:00	2020-01-10 00:00:00	SCHEDULED	\N	\N	1	\N	6769077249719871953	\N	{}	PUBLIC	'gegenantrag':1A 'pp001':3A 'pp002':4A
6769077249786746253	Noch ein Gegenantrag zu PP001 mit Volltextsuche	will was ganz anderes, ich will Volltextsuche			PP003	2020-01-03 00:00:00	2020-01-09 00:00:00	2020-01-24 00:00:00	SCHEDULED	\N	\N	1	\N	6769077249719871953	\N	{}	PUBLIC	'ganz':10C 'gegenantrag':3A 'pp001':5A 'pp003':15A 'volltextsuch':7A,14C
6769077249785839928	Abgelehnter Gegenantrag zum Verschobenen Antrag PP007	Gegenantrag von PP008			PP008	2020-01-06 00:00:00	2020-01-06 00:00:00	2020-01-11 00:00:00	FINISHED	\N	\N	10	6769077249766705726	\N	http://example.com	{}	PUBLIC	'abgelehnt':1A 'antrag':5A 'gegenantrag':2A,7C 'pp007':6A 'pp008':9C,10A 'verschob':4A
\.


--
-- Data for Name: propositiontags; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.propositiontags (proposition_id, tag_id) FROM stdin;
6769077249737786120	1
6769077249744553781	1
6769077249745788325	1
6769077249719871953	2
6769077249719871953	3
6769077249757422710	1
6769077249765775280	1
6769077249768528865	1
6769077249766705726	1
6769077249785839928	1
\.


--
-- Data for Name: propositiontypes; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.propositiontypes (id, name, abbreviation, description, policy_id) FROM stdin;
1	Positionspapier	PP	1 Küstenwache vor Lesbos «Wir entscheiden, wer stirbt» 2 Deutscher Altkanzler schwer erkrankt Helmut Schmidt (96) «ist nicht.. 14:44 dpa-AFX: HSBC belässt Deutsche Telekom auf 'Buy' - Ziel 19 Euro 01.12. 1903 kreierte Kolo Moser eine Wohnungseinrichtung, die nun in aller Welt verstreut ist: in Museums- und in Privatbesitz.	1
2	Wahlprogrammantrag	WP	174459 Bomber Sukhoi T-4: 100 Tonnen schwer und schneller als der SchallJagdflugzeuge sind in der Regel schneller als Bomber. 18:25 Uhr Audi-Duell: Di Grassi an Lotterer vorbei Lucas di Grassi ist hier schneller unterwegs als Andre Lotterer. 17,175 Millionen Aktien bringt Ferraris Mutterkonzern Fiat Chrysler (FCA) zu einem Preis zwischen 48 und 52 Dollar auf den Markt.	1
\.


--
-- Data for Name: secretvoters; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.secretvoters (member_id, ballot_id, status, last_change) FROM stdin;
\.


--
-- Data for Name: subjectareas; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.subjectareas (id, name, description, department_id) FROM stdin;
1	Allgemein	\N	3
2	Innerparteiliches	\N	4
3	Politik	\N	4
4	Innerparteiliches	\N	5
\.


--
-- Data for Name: supporters; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.supporters (member_id, proposition_id, submitter, status, last_change) FROM stdin;
2	6769077249719871953	t	ACTIVE	2021-02-21 02:16:19.662801
3	6769077249780739847	t	ACTIVE	2021-02-21 02:16:19.662801
2	6769077249757422710	f	ACTIVE	2021-02-21 02:16:19.662801
2	6769077249765775280	f	ACTIVE	2021-02-21 02:16:19.662801
2	6769077249768528865	f	ACTIVE	2021-02-21 02:16:19.662801
2	6769077249766705726	f	ACTIVE	2021-02-21 02:16:19.662801
3	6769077249719871953	f	RETRACTED	2021-02-21 02:16:19.662801
3	6769077249757422710	f	EXPIRED	2021-02-21 02:16:19.662801
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.tags (id, name, parent_id, mut_exclusive) FROM stdin;
1	Täääg3	\N	f
2	Tag1	\N	f
3	Tag2	\N	f
\.


--
-- Data for Name: urns; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.urns (id, voting_id, accepted, location, description, opening) FROM stdin;
\.


--
-- Data for Name: urnsupporters; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.urnsupporters (member_id, urn_id, type, voted) FROM stdin;
\.


--
-- Data for Name: user_login_token; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.user_login_token (token, user_id, valid_until) FROM stdin;
\.


--
-- Data for Name: userpassword; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.userpassword (user_id, hashed_password) FROM stdin;
1	admin
2	test
\.


--
-- Data for Name: userprofiles; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.userprofiles (id, sub, eligible, verified, profile) FROM stdin;
3	sub_egon	t	t	ich halt
4	sub_olaf	f	t	## Markdown\n\nText
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.users (id, name, email, auth_type, joined, active, last_active, can_login_until) FROM stdin;
1	testadmin	\N	system	2021-02-21 02:16:19.662801	t	2021-02-21 02:16:19.662801	\N
2	testuser	\N	system	2021-02-21 02:16:19.662801	t	2021-02-21 02:16:19.662801	\N
3	egon	\N	oauth	2021-02-21 02:16:19.662801	t	2021-02-21 02:16:19.662801	\N
4	depadmin	\N	oauth	2021-02-21 02:16:19.662801	t	2021-02-21 02:16:19.662801	\N
\.


--
-- Data for Name: voting_module; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.voting_module (id, name, description, base_url, module_type) FROM stdin;
\.


--
-- Data for Name: voting_phase_types; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.voting_phase_types (id, name, abbreviation, secret_voting_possible, voting_type) FROM stdin;
1	Bundesparteitag	BPT	t	ASSEMBLY
2	Online-Urabstimmung	UR	f	ONLINE
\.


--
-- Data for Name: votingphases; Type: TABLE DATA; Schema: public; Owner: ekklesia
--

COPY public.votingphases (id, status, target, department_id, phase_type_id, secret, name, title, description, voting_module_data) FROM stdin;
1	SCHEDULED	2020-11-11 00:00:00	3	1	t	bpt201	BPT 2020.1	Der nächste Parteitag irgendwo	{}
2	PREPARING	\N	5	2	f	ur19+	Urabstimmung 2019+	eine **Urabstimmung** in Zentalschweiz	{}
3	FINISHED	2019-11-10 00:00:00	3	1	t	bpt192	BPT 2019.2	Der BPT in Bad Homburg	{}
\.


--
-- Name: argumentrelations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.argumentrelations_id_seq', 3, true);


--
-- Name: arguments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.arguments_id_seq', 3, true);


--
-- Name: ballots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.ballots_id_seq', 10, true);


--
-- Name: changeset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.changeset_id_seq', 1, false);


--
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.departments_id_seq', 5, true);


--
-- Name: document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.document_id_seq', 1, true);


--
-- Name: groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.groups_id_seq', 2, true);


--
-- Name: policies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.policies_id_seq', 1, true);


--
-- Name: propositiontypes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.propositiontypes_id_seq', 2, true);


--
-- Name: subjectareas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.subjectareas_id_seq', 4, true);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.tags_id_seq', 3, true);


--
-- Name: urns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.urns_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: voting_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.voting_module_id_seq', 1, false);


--
-- Name: voting_phase_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.voting_phase_types_id_seq', 2, true);


--
-- Name: votingphases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ekklesia
--

SELECT pg_catalog.setval('public.votingphases_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: areamembers pk_areamembers; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.areamembers
    ADD CONSTRAINT pk_areamembers PRIMARY KEY (area_id, member_id);


--
-- Name: argumentrelations pk_argumentrelations; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentrelations
    ADD CONSTRAINT pk_argumentrelations PRIMARY KEY (id);


--
-- Name: arguments pk_arguments; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.arguments
    ADD CONSTRAINT pk_arguments PRIMARY KEY (id);


--
-- Name: argumentvotes pk_argumentvotes; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentvotes
    ADD CONSTRAINT pk_argumentvotes PRIMARY KEY (member_id, relation_id);


--
-- Name: ballots pk_ballots; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.ballots
    ADD CONSTRAINT pk_ballots PRIMARY KEY (id);


--
-- Name: changeset pk_changeset; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.changeset
    ADD CONSTRAINT pk_changeset PRIMARY KEY (id);


--
-- Name: customizable_text pk_customizable_text; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.customizable_text
    ADD CONSTRAINT pk_customizable_text PRIMARY KEY (name, lang);


--
-- Name: departmentmembers pk_departmentmembers; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.departmentmembers
    ADD CONSTRAINT pk_departmentmembers PRIMARY KEY (department_id, member_id);


--
-- Name: departments pk_departments; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT pk_departments PRIMARY KEY (id);


--
-- Name: document pk_document; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT pk_document PRIMARY KEY (id);


--
-- Name: groupmembers pk_groupmembers; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.groupmembers
    ADD CONSTRAINT pk_groupmembers PRIMARY KEY (group_id, member_id);


--
-- Name: groups pk_groups; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT pk_groups PRIMARY KEY (id);


--
-- Name: oauth_token pk_oauth_token; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.oauth_token
    ADD CONSTRAINT pk_oauth_token PRIMARY KEY (id);


--
-- Name: page pk_page; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.page
    ADD CONSTRAINT pk_page PRIMARY KEY (name, lang);


--
-- Name: policies pk_policies; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.policies
    ADD CONSTRAINT pk_policies PRIMARY KEY (id);


--
-- Name: postalvotes pk_postalvotes; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.postalvotes
    ADD CONSTRAINT pk_postalvotes PRIMARY KEY (member_id, voting_id);


--
-- Name: propositionnotes pk_propositionnotes; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositionnotes
    ADD CONSTRAINT pk_propositionnotes PRIMARY KEY (proposition_id, user_id);


--
-- Name: propositions pk_propositions; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositions
    ADD CONSTRAINT pk_propositions PRIMARY KEY (id);


--
-- Name: propositiontags pk_propositiontags; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontags
    ADD CONSTRAINT pk_propositiontags PRIMARY KEY (proposition_id, tag_id);


--
-- Name: propositiontypes pk_propositiontypes; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontypes
    ADD CONSTRAINT pk_propositiontypes PRIMARY KEY (id);


--
-- Name: secretvoters pk_secretvoters; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.secretvoters
    ADD CONSTRAINT pk_secretvoters PRIMARY KEY (member_id, ballot_id);


--
-- Name: subjectareas pk_subjectareas; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.subjectareas
    ADD CONSTRAINT pk_subjectareas PRIMARY KEY (id);


--
-- Name: supporters pk_supporters; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.supporters
    ADD CONSTRAINT pk_supporters PRIMARY KEY (member_id, proposition_id);


--
-- Name: tags pk_tags; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT pk_tags PRIMARY KEY (id);


--
-- Name: urns pk_urns; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.urns
    ADD CONSTRAINT pk_urns PRIMARY KEY (id);


--
-- Name: urnsupporters pk_urnsupporters; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.urnsupporters
    ADD CONSTRAINT pk_urnsupporters PRIMARY KEY (member_id, urn_id);


--
-- Name: user_login_token pk_user_login_token; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.user_login_token
    ADD CONSTRAINT pk_user_login_token PRIMARY KEY (token);


--
-- Name: userpassword pk_userpassword; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.userpassword
    ADD CONSTRAINT pk_userpassword PRIMARY KEY (user_id);


--
-- Name: userprofiles pk_userprofiles; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.userprofiles
    ADD CONSTRAINT pk_userprofiles PRIMARY KEY (id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- Name: voting_module pk_voting_module; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.voting_module
    ADD CONSTRAINT pk_voting_module PRIMARY KEY (id);


--
-- Name: voting_phase_types pk_voting_phase_types; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.voting_phase_types
    ADD CONSTRAINT pk_voting_phase_types PRIMARY KEY (id);


--
-- Name: votingphases pk_votingphases; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.votingphases
    ADD CONSTRAINT pk_votingphases PRIMARY KEY (id);


--
-- Name: departments uq_departments_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT uq_departments_name UNIQUE (name);


--
-- Name: document uq_document_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT uq_document_name UNIQUE (name, lang, area_id);


--
-- Name: groups uq_groups_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT uq_groups_name UNIQUE (name);


--
-- Name: policies uq_policies_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.policies
    ADD CONSTRAINT uq_policies_name UNIQUE (name);


--
-- Name: propositiontypes uq_propositiontypes_abbreviation; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontypes
    ADD CONSTRAINT uq_propositiontypes_abbreviation UNIQUE (abbreviation);


--
-- Name: propositiontypes uq_propositiontypes_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontypes
    ADD CONSTRAINT uq_propositiontypes_name UNIQUE (name);


--
-- Name: tags uq_tags_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT uq_tags_name UNIQUE (name);


--
-- Name: userprofiles uq_userprofiles_sub; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.userprofiles
    ADD CONSTRAINT uq_userprofiles_sub UNIQUE (sub);


--
-- Name: users uq_users_email; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_email UNIQUE (email);


--
-- Name: users uq_users_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_name UNIQUE (name);


--
-- Name: voting_module uq_voting_module_name; Type: CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.voting_module
    ADD CONSTRAINT uq_voting_module_name UNIQUE (name);


--
-- Name: ix_propositions_search_vector; Type: INDEX; Schema: public; Owner: ekklesia
--

CREATE INDEX ix_propositions_search_vector ON public.propositions USING gin (search_vector);


--
-- Name: propositions propositions_search_vector_trigger; Type: TRIGGER; Schema: public; Owner: ekklesia
--

CREATE TRIGGER propositions_search_vector_trigger BEFORE INSERT OR UPDATE ON public.propositions FOR EACH ROW EXECUTE FUNCTION public.propositions_search_vector_update();


--
-- Name: areamembers fk_areamembers_area_id_subjectareas; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.areamembers
    ADD CONSTRAINT fk_areamembers_area_id_subjectareas FOREIGN KEY (area_id) REFERENCES public.subjectareas(id);


--
-- Name: areamembers fk_areamembers_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.areamembers
    ADD CONSTRAINT fk_areamembers_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: argumentrelations fk_argumentrelations_argument_id_arguments; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentrelations
    ADD CONSTRAINT fk_argumentrelations_argument_id_arguments FOREIGN KEY (argument_id) REFERENCES public.arguments(id);


--
-- Name: argumentrelations fk_argumentrelations_parent_id_argumentrelations; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentrelations
    ADD CONSTRAINT fk_argumentrelations_parent_id_argumentrelations FOREIGN KEY (parent_id) REFERENCES public.argumentrelations(id);


--
-- Name: argumentrelations fk_argumentrelations_proposition_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentrelations
    ADD CONSTRAINT fk_argumentrelations_proposition_id_propositions FOREIGN KEY (proposition_id) REFERENCES public.propositions(id);


--
-- Name: arguments fk_arguments_author_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.arguments
    ADD CONSTRAINT fk_arguments_author_id_users FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: argumentvotes fk_argumentvotes_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentvotes
    ADD CONSTRAINT fk_argumentvotes_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: argumentvotes fk_argumentvotes_relation_id_argumentrelations; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.argumentvotes
    ADD CONSTRAINT fk_argumentvotes_relation_id_argumentrelations FOREIGN KEY (relation_id) REFERENCES public.argumentrelations(id);


--
-- Name: ballots fk_ballots_area_id_subjectareas; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.ballots
    ADD CONSTRAINT fk_ballots_area_id_subjectareas FOREIGN KEY (area_id) REFERENCES public.subjectareas(id);


--
-- Name: ballots fk_ballots_proposition_type_id_propositiontypes; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.ballots
    ADD CONSTRAINT fk_ballots_proposition_type_id_propositiontypes FOREIGN KEY (proposition_type_id) REFERENCES public.propositiontypes(id);


--
-- Name: ballots fk_ballots_voting_id_votingphases; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.ballots
    ADD CONSTRAINT fk_ballots_voting_id_votingphases FOREIGN KEY (voting_id) REFERENCES public.votingphases(id);


--
-- Name: changeset fk_changeset_document_id_document; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.changeset
    ADD CONSTRAINT fk_changeset_document_id_document FOREIGN KEY (document_id) REFERENCES public.document(id);


--
-- Name: changeset fk_changeset_proposition_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.changeset
    ADD CONSTRAINT fk_changeset_proposition_id_propositions FOREIGN KEY (proposition_id) REFERENCES public.propositions(id);


--
-- Name: departmentmembers fk_departmentmembers_department_id_departments; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.departmentmembers
    ADD CONSTRAINT fk_departmentmembers_department_id_departments FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: departmentmembers fk_departmentmembers_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.departmentmembers
    ADD CONSTRAINT fk_departmentmembers_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: document fk_document_area_id_subjectareas; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT fk_document_area_id_subjectareas FOREIGN KEY (area_id) REFERENCES public.subjectareas(id);


--
-- Name: document fk_document_proposition_type_id_propositiontypes; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT fk_document_proposition_type_id_propositiontypes FOREIGN KEY (proposition_type_id) REFERENCES public.propositiontypes(id);


--
-- Name: groupmembers fk_groupmembers_group_id_groups; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.groupmembers
    ADD CONSTRAINT fk_groupmembers_group_id_groups FOREIGN KEY (group_id) REFERENCES public.groups(id);


--
-- Name: groupmembers fk_groupmembers_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.groupmembers
    ADD CONSTRAINT fk_groupmembers_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: oauth_token fk_oauth_token_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.oauth_token
    ADD CONSTRAINT fk_oauth_token_id_users FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: postalvotes fk_postalvotes_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.postalvotes
    ADD CONSTRAINT fk_postalvotes_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: postalvotes fk_postalvotes_voting_id_votingphases; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.postalvotes
    ADD CONSTRAINT fk_postalvotes_voting_id_votingphases FOREIGN KEY (voting_id) REFERENCES public.votingphases(id);


--
-- Name: propositionnotes fk_propositionnotes_proposition_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositionnotes
    ADD CONSTRAINT fk_propositionnotes_proposition_id_propositions FOREIGN KEY (proposition_id) REFERENCES public.propositions(id);


--
-- Name: propositionnotes fk_propositionnotes_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositionnotes
    ADD CONSTRAINT fk_propositionnotes_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: propositions fk_propositions_author_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositions
    ADD CONSTRAINT fk_propositions_author_id_users FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: propositions fk_propositions_ballot_id_ballots; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositions
    ADD CONSTRAINT fk_propositions_ballot_id_ballots FOREIGN KEY (ballot_id) REFERENCES public.ballots(id);


--
-- Name: propositions fk_propositions_modifies_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositions
    ADD CONSTRAINT fk_propositions_modifies_id_propositions FOREIGN KEY (modifies_id) REFERENCES public.propositions(id);


--
-- Name: propositions fk_propositions_replaces_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositions
    ADD CONSTRAINT fk_propositions_replaces_id_propositions FOREIGN KEY (replaces_id) REFERENCES public.propositions(id);


--
-- Name: propositiontags fk_propositiontags_proposition_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontags
    ADD CONSTRAINT fk_propositiontags_proposition_id_propositions FOREIGN KEY (proposition_id) REFERENCES public.propositions(id);


--
-- Name: propositiontags fk_propositiontags_tag_id_tags; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontags
    ADD CONSTRAINT fk_propositiontags_tag_id_tags FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: propositiontypes fk_propositiontypes_policy_id_policies; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.propositiontypes
    ADD CONSTRAINT fk_propositiontypes_policy_id_policies FOREIGN KEY (policy_id) REFERENCES public.policies(id);


--
-- Name: secretvoters fk_secretvoters_ballot_id_ballots; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.secretvoters
    ADD CONSTRAINT fk_secretvoters_ballot_id_ballots FOREIGN KEY (ballot_id) REFERENCES public.ballots(id);


--
-- Name: secretvoters fk_secretvoters_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.secretvoters
    ADD CONSTRAINT fk_secretvoters_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: subjectareas fk_subjectareas_department_id_departments; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.subjectareas
    ADD CONSTRAINT fk_subjectareas_department_id_departments FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: supporters fk_supporters_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.supporters
    ADD CONSTRAINT fk_supporters_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: supporters fk_supporters_proposition_id_propositions; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.supporters
    ADD CONSTRAINT fk_supporters_proposition_id_propositions FOREIGN KEY (proposition_id) REFERENCES public.propositions(id);


--
-- Name: tags fk_tags_parent_id_tags; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT fk_tags_parent_id_tags FOREIGN KEY (parent_id) REFERENCES public.tags(id);


--
-- Name: urns fk_urns_voting_id_votingphases; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.urns
    ADD CONSTRAINT fk_urns_voting_id_votingphases FOREIGN KEY (voting_id) REFERENCES public.votingphases(id);


--
-- Name: urnsupporters fk_urnsupporters_member_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.urnsupporters
    ADD CONSTRAINT fk_urnsupporters_member_id_users FOREIGN KEY (member_id) REFERENCES public.users(id);


--
-- Name: urnsupporters fk_urnsupporters_urn_id_urns; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.urnsupporters
    ADD CONSTRAINT fk_urnsupporters_urn_id_urns FOREIGN KEY (urn_id) REFERENCES public.urns(id);


--
-- Name: user_login_token fk_user_login_token_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.user_login_token
    ADD CONSTRAINT fk_user_login_token_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: userpassword fk_userpassword_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.userpassword
    ADD CONSTRAINT fk_userpassword_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: userprofiles fk_userprofiles_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.userprofiles
    ADD CONSTRAINT fk_userprofiles_id_users FOREIGN KEY (id) REFERENCES public.users(id);


--
-- Name: votingphases fk_votingphases_department_id_departments; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.votingphases
    ADD CONSTRAINT fk_votingphases_department_id_departments FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: votingphases fk_votingphases_phase_type_id_voting_phase_types; Type: FK CONSTRAINT; Schema: public; Owner: ekklesia
--

ALTER TABLE ONLY public.votingphases
    ADD CONSTRAINT fk_votingphases_phase_type_id_voting_phase_types FOREIGN KEY (phase_type_id) REFERENCES public.voting_phase_types(id);


--
-- PostgreSQL database dump complete
--

